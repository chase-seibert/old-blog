---
layout: post
title: Flask-Admin Edit One To Many Fields from the List View
tags: python flask
---

I got to play with [Flask-Admin](https://flask-admin.readthedocs.org/en/latest/) for the first time
this week. Compared with Django admin, it's very extensible, though the default UI is pretty ugly.
In any case, I ran into one particular challenge that took a good deal longer to figure out than
it should have. Specifically, making a one to many relationship editable from the list view.

on the `ModelView`. 
You can easily expose editable fields from the list view using `column_editable_list`. See
[the documentation](https://flask-admin.readthedocs.org/en/latest/api/mod_model/#flask_admin.model.BaseModelView.column_editable_list)
for more.

```python
class MyModelView(BaseModelView):
    column_editable_list = ('question', 'details', 'status')
```    

This ends up looking like this:

![column_editable_list](/blog/images/column_editable_list.png)

This works for most `db.Model` column types I tried. For `String`, `Text` and `Integer`, you get a 
simple `input` HTML element. For basic many to one relationships, you get a `select` HTML element.
But when I tried to make a one to many relationship editable, I got a stack trace:

```bash
Traceback (most recent call last):
  File "/srv/nerdwallet/myproject/venv/lib/python2.7/site-packages/flask/app.py", line 1836, in __call__
    return self.wsgi_app(environ, start_response)
  ...
  File "/srv/nerdwallet/myproject/venv/lib/python2.7/site-packages/wtforms/fields/core.py", line 149, in __call__
    return self.meta.render_field(self, kwargs)
  File "/srv/nerdwallet/myproject/venv/lib/python2.7/site-packages/wtforms/meta.py", line 53, in render_field
    return field.widget(field, **render_kw)
  File "/srv/nerdwallet/myproject/venv/lib/python2.7/site-packages/flask_admin/model/widgets.py", line 93, in __call__
    kwargs = self.get_kwargs(subfield, kwargs)
  File "/srv/nerdwallet/myproject/venv/lib/python2.7/site-packages/flask_admin/model/widgets.py", line 148, in get_kwargs
    raise Exception('Unsupported field type: %s' % (type(subfield),))
Exception: Unsupported field type: <class 'flask_admin.contrib.sqla.fields.QuerySelectMultipleField'>
```

The model column definition in question was a simple relationship with a join table:

```python
class MyModel(AAAModel):
    ...
    # uselist=True means you can have more than one child MyChildModel per MyModel
    children = relationship('MyChildModel', secondary='model_children_join', uselist=True)
```

Looking into the [Flask-Admin code](https://github.com/flask-admin/flask-admin/blob/master/flask_admin/model/widgets.py#L100), 
they actually support a number of other fields types such as `Boolean`, `DateTime`, `Float`, etc. But
no select multiple. Here is the `Flask-Admin` code block that I was looking at:

```python
class XEditableWidget(object):
    """
        WTForms widget that provides in-line editing for the list view.

        Determines how to display the x-editable/ajax form based on the
        field inside of the FieldList (StringField, IntegerField, etc).
    """
    def __call__(self, field, **kwargs):
        kwargs.setdefault('data-value', kwargs.pop('value', ''))

        kwargs.setdefault('data-role', 'x-editable')
        kwargs.setdefault('data-url', './ajax/update/')

        kwargs.setdefault('id', field.id)
        kwargs.setdefault('name', field.name)
        kwargs.setdefault('href', '#')

        if not kwargs.get('pk'):
            raise Exception('pk required')
        kwargs['data-pk'] = str(kwargs.pop("pk"))

        kwargs['data-csrf'] = kwargs.pop("csrf", "")

        # subfield is the first entry (subfield) from FieldList (field)
        subfield = field.entries[0]

        kwargs = self.get_kwargs(subfield, kwargs)

        return HTMLString(
            '<a %s>%s</a>' % (html_params(**kwargs),
                              escape(kwargs['data-value']))
        )

    def get_kwargs(self, subfield, kwargs):
        """
            Return extra kwargs based on the subfield type.
        """
        if subfield.type == 'StringField':
            kwargs['data-type'] = 'text'
        elif subfield.type == 'TextAreaField':
            kwargs['data-type'] = 'textarea'
            kwargs['data-rows'] = '5'
        elif subfield.type == 'BooleanField':
            kwargs['data-type'] = 'select'
            # data-source = dropdown options
            kwargs['data-source'] = {'': 'False', '1': 'True'}
            kwargs['data-role'] = 'x-editable-boolean'
        elif subfield.type == 'Select2Field':
            kwargs['data-type'] = 'select'
            kwargs['data-source'] = dict(subfield.choices)
        elif subfield.type == 'DateField':
            kwargs['data-type'] = 'combodate'
            kwargs['data-format'] = 'YYYY-MM-DD'
            kwargs['data-template'] = 'YYYY-MM-DD'
        elif subfield.type == 'DateTimeField':
            kwargs['data-type'] = 'combodate'
            kwargs['data-format'] = 'YYYY-MM-DD HH:mm:ss'
            kwargs['data-template'] = 'YYYY-MM-DD  HH:mm:ss'
            # x-editable-combodate uses 1 minute increments
            kwargs['data-role'] = 'x-editable-combodate'
        elif subfield.type == 'TimeField':
            kwargs['data-type'] = 'combodate'
            kwargs['data-format'] = 'HH:mm:ss'
            kwargs['data-template'] = 'HH:mm:ss'
            kwargs['data-role'] = 'x-editable-combodate'
        elif subfield.type == 'IntegerField':
            kwargs['data-type'] = 'number'
        elif subfield.type in ['FloatField', 'DecimalField']:
            kwargs['data-type'] = 'number'
            kwargs['data-step'] = 'any'
        elif subfield.type in ['QuerySelectField', 'ModelSelectField']:
            kwargs['data-type'] = 'select'

            choices = {}
            for choice in subfield:
                try:
                    choices[str(choice._value())] = str(choice.label.text)
                except TypeError:
                    choices[str(choice._value())] = ""
            kwargs['data-source'] = choices
        else:
            raise Exception('Unsupported field type: %s' % (type(subfield),))

        # for Select2, QuerySelectField, and ModelSelectField
        if getattr(subfield, 'allow_blank', False):
            kwargs['data-source']['__None'] = ""

        return kwargs
```

Basically, it's generating some HTML from a `kwargs` dict based on the field type. These are 
[WTForms](https://wtforms.readthedocs.org/en/latest/) types from the 
[SQLAlchemy WTForm extension](https://wtforms.readthedocs.org/en/latest/ext.html?highlight=queryselectfield#module-wtforms.ext.sqlalchemy). 
But the `data-type` types are actually from a Javascript library called [x-editable](https://vitalets.github.io/x-editable/docs.html), which is
doing the actual UI and Ajax call for the update. 

It turns out that `x-editable` doesn't support a `select multiple` element, but they do have a [checklist](https://vitalets.github.io/x-editable/docs.html#checklist)
type, which is just as good (at least for a small number of choices). Hacking this into the 
`ModelView` was pretty simple.

```python
from flask.ext.admin.model.widgets import XEditableWidget


class CustomWidget(XEditableWidget):

    def get_kwargs(self, subfield, kwargs):
        if subfield.type == 'QuerySelectMultipleField':
            kwargs['data-type'] = 'checklist'
            kwargs['data-placement'] = 'left'
            # copied from flask_admin/model/widgets.py
            choices = {}
            for choice in subfield:
                try:
                    choices[str(choice._value())] = str(choice.label.text)
                except TypeError:
                    choices[str(choice._value())] = ""
            kwargs['data-source'] = choices
        else:
            super(CustomWidget, self).get_kwargs(subfield, kwargs)
        return kwargs


class CustomFieldList(ListEditableFieldList):
    widget = CustomWidget()
    
class MyModelView(BaseModelView):
    column_editable_list = ('question', 'details', 'slug', 'status', 'children')

    def get_list_form(self):
        return self.scaffold_list_form(CustomFieldList)
```

