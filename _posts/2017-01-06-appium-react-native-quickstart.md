---
layout: post
title: Appium + React Native Quickstart
tags:
---

[Appium](http://appium.io/) is a great framework for automated functional testing
of mobile apps. But it's very general purpose, meaning that there is relatively
little documentation for specific mobile app architectures. It's also fairly
complicated. Being "Selenium for mobile", and leveraging a lot of existing
Selenium architecture, it requires a lot of context to get up and running.
This is a guide for getting starting testing a React Native app on Appium,
without assuming too much prior knowledge.

# Moving Pieces

At a high level, you write code in any number of supported languages that
comprise your tests. You can use your existing test framework, i.e. py.test for
Python, Mocha for JavaScript, whatever you want. In your test bootstrapping, you
are going to instantiate a Appium "web driver"[1] client, and configure it. The
driver will connect to a running `appium` service, which you will have installed
and kicked off in the background. Down the line, you can get a vendor like
[SauceLabs](https://saucelabs.com/) or [AWS Device Farm](https://aws.amazon.com/device-farm/)
to run that in the cloud if you want.

In your tests, you use the driver to tell the appium service to launch your app
in a simulator. Eventually, you can also tell it to run on a physical device. You
give it a path to your app `.app` file for iOS, or the `.apk` for Android, and it
can either re-use an emulator that you've already launched on your desktop, or
start one.

Once the app loads, you issue commands to the driver to perform certain actions
inside the app. Common examples are clicking on buttons or links, entering data
into forms and checking for content on the screen. Those checks are essentially
the asserts in your tests. If at any point your tests cannot locate the item
that it's expecting on the screen, you will get an exception and that test will
fail.

[1] The term "web driver" is a historical hold over from Selenium.

## Potentially Confusing Parts & Gotchas

I've written some Selenium test suites in the past, but it's been a while. I
remember having some of the same initial confusions with Appium.

- The `appium` service needs to be launched and run in the background; your
tests do not kick that off for you.
- You can start your emulator manually and have Appium connect to that instance.
It happens automatically, for Android anyway.

# Installing Stuff

Appium's [getting started](http://appium.io/getting-started.html) doc has a
surprising amount of confusing cruft on it, but you should reference it for the
latest instructions.

As of 2017-01-16, this is a TL;DR version to get you started with everything
you need for both iOS and Android.

```bash
brew install libimobiledevice --HEAD
brew install carthage
brew install node
npm install -g appium
npm install wd
npm install -g ios-deploy
gem install xcpretty  # optional
appium
```

That should get you a running `appium` process. Just leave it open in a tab.

Example output:

```bash
[Appium] Welcome to Appium v1.6.3
[Appium] Appium REST http interface listener started on 0.0.0.0:4723
```

# Running a Dummy Test

*Note: Your React Native app build should be in production mode. Otherwise,
selecting elements on the page will be super crazy slow. You can validate that
you're in the right mode by killing your packager; the production builds should
have all the JS assets packaged into the app.*

Before getting into the full blown details of how to write a full test, I found
that I first just wanted to make sure I could write some code that launched my
app correctly in the emulator. I suggest starting with Android if possible; iOS
apps under XCode 8 and later required a [bunch of additional moving pieces](https://github.com/appium/appium-xcuitest-driver).

Appium has a bunch of [sample client code](https://github.com/appium/sample-code/tree/master/sample-code/examples)
for various languages. I found it to be too much; it's hard to tell what's abstracted
where, and if you don't know the test runner they have chosen, there may be
additional learning curve. I'm going give you a very simple example in Python.

**Note: we're assuming that your app has a link with specific text in it on the
first screen, and clicking that links loads a second page with more specific
text on it.**

First, you need to install the Python client:

```bash
virtualenv venv
. venv/bin/activate
pip install Appium-Python-Client
```

Then, create a file called `test.py`:

```python
import os
import time
from appium import webdriver

driver = webdriver.Remote(
    command_executor='http://127.0.0.1:4723/wd/hub',
    desired_capabilities={
        'app': os.path.expanduser('~/Downloads/app-release.apk'),
        'platformName': 'Android',
        'deviceName': 'Nexus 6P API 25',
    })

# wait for app to load
time.sleep(10)

# find the link with the text "Click here" and click on it
link = driver.find_element_by_xpath('//*[@text="Click Here"]')
link.click()

# wait for the next screen to load
time.sleep(10)

# make sure the correct "Success" result is on the page
driver.find_element_by_xpath('//*[@text="Success"]')

# important; you will not be able to launch again if this does not happen
driver.quit()
```

This is terrible code, but it should launch your app, in any case. From there
you can start to play around with it. Try inserting a `import pdb; pdb.set_trace`
before the first `sleep` to get an interactive repl where you can try querying
for selectors.

# Writing Tests

You might notice that we're using a bunch of sleeps. That's a common anti-pattern
in both Selenium and Appium; you don't want to rely on indeterministic page loading
timing. We're also using xpath selectors. I don't know about you, but I never want
to write another one of those. Let's explore some options.

## Useful Patterns

My goal here is to make individual tests as simple to define as possible, and to
remove boilerplate, waits and finicky selectors from them.

### A Base Test Class

It's common to have a base class for all your functional tests that does the basic
starting the simulator and loading of the app. But it's also useful as a place to
put re-usable methods for making writing tests easier.

Replace the contents of your `test.py`:

```python
import os
import unittest
from appium import webdriver


class AppiumTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723/wd/hub',
            desired_capabilities={
              'app': os.path.abspath('~/Downloads/app-release.apk'),
              'platformName': 'Android',
              'deviceName': 'Nexus 6P API 25',
        })

    def tearDown(self):
        self.driver.quit()


class ExampleTests(AppiumTest):

    def test_login(self):
      assert True        
```        

If you're using `py.test` (avaiable with `pip install pytest`), then you can run
your example test with the command `py.test test.py`.

## Selectors

The hardest part of writing tests is figuring out how to locate the elements on
the screen that you need to interact with, or validate. Whether you're dealing with
iOS or Android, Appium exposes an XML DOM that represents what's currently on
the screen. You can actually see the full DOM at any time by evaluating
`driver.page_source`. It get's pretty complicated quickly. Here is vastly
simplified example:

```xml
<?xml version="1.0" ?>
<hierarchy rotation="0">
	<android.widget.FrameLayout bounds="[0,0][1440,2392]" checkable="false" checked="false" class="android.widget.FrameLayout" clickable="false" content-desc="" enabled="true" focusable="false" focused="false" index="0" instance="0" long-clickable="false" package="com.myapp" password="false" resource-id="" scrollable="false" selected="false" text="">
		<android.widget.LinearLayout bounds="[0,0][1440,2392]" checkable="false" checked="false" class="android.widget.LinearLayout" clickable="false" content-desc="" enabled="true" focusable="false" focused="false" index="0" instance="0" long-clickable="false" package="com.myapp" password="false" resource-id="" scrollable="false" selected="false" text="">
  		<android.view.ViewGroup bounds="[0,224][1440,1655]" checkable="false" checked="false" class="android.view.ViewGroup" clickable="false" content-desc="" enabled="true" focusable="true" focused="false" index="0" instance="6" long-clickable="false" package="com.myapp" password="false" resource-id="" scrollable="false" selected="false" text="">
  			<android.widget.TextView bounds="[53,224][1388,298]" checkable="false" checked="false" class="android.widget.TextView" clickable="false" content-desc="" enabled="true" focusable="false" focused="false" index="0" instance="0" long-clickable="false" package="com.myapp" password="false" resource-id="" scrollable="false" selected="false" text="Sign in"/>
  		</android.view.ViewGroup>
		</android.widget.LinearLayout>
		<android.view.View bounds="[0,2392][1440,2560]" checkable="false" checked="false" class="android.view.View" clickable="false" content-desc="" enabled="true" focusable="false" focused="false" index="1" instance="0" long-clickable="false" package="com.myapp" password="false" resource-id="android:id/navigationBarBackground" scrollable="false" selected="false" text=""/>
	</android.widget.FrameLayout>
</hierarchy>
```

### XPath

See the `TextView` element with the text `Sign in`? If you want to locate that
element, you can select it using XPath:

```python
link = driver.find_element_by_xpath('//*[@text="Sign in"]')
```

This selector looks for any DOM element (`*`) that has a `text` attribute of
"Sign in". What if there is more than one on the page? You can use
`find_elements_by_xpath` (notice the plural "s" on elements) to get the full
list, and these pick the right one by index.

XPath is somewhat finicky. As your DOM changes, hardcoded text values and
especially indexes for multiple matches will change often. This will break
your tests.


### Accessibility Labels

A better option is to put IDs on elements and use a selector for that specific ID.
Typically, options here are test IDs, test tags and accessibility labels. Until
React Native [implements test IDs](https://github.com/facebook/react-native/pull/9942),
or Appium [supports test tags](https://discuss.appium.io/t/react-native-ui-element-access-via-testid/7845/5),
the only option here is accessibility labels.

In your React Native code, you can add the `accessibilityLabel` to any `View`
element. *Note: these are ONLY for View elements, you will likely end up wrapping
other elements in a View often.*

```xml
<View accessibilityLabel="Sign in here">
  <Link
    onPress={this.selectOnboardingType.bind(this, 'signin')}
    style={styles.link}
    id="signin"
  >
    {I18n.t('signInTitle')}
  </Link>
</View>
```

**Note: Accessibility labels ARE user visible; they are used for disabled users.
So you need to make sure they are human readable and make sense.**

Then, in your test, you can use the

```python
link_view = driver.find_elements_by_accessibility_id("Sign in here")
```

You can typically interact with the `View` object directly for clicking and
sending user input. If that doesn't work, you can use `link_view.find_element_by_xpath`
method to query for it's children.

See [Appium documentation](http://appium.io/slate/en/0.18.x/?javascript#ios-only) for
other selector strategies. [More](http://appium.wikia.com/wiki/Finding_Elements).


## Waits

I've found that a useful pattern for avoiding sleeps is to instead wait for an
expected element to show up on the screen. You define a total time you're willing
to wait, such as 10 seconds, and a short time interval that you want to poll the
screen on, say 200 milliseconds.

This is exactly what Selenium's `WebDriverWait` module does. But I'm going to
show you a basic implementation.


## Putting it all together

Ideally, I want my actual test cases to be very concise. Here is an example:

```python
def test_login(self):
    self.wait_until('Please enter your login', partial=True)
    self.get('#Email').send_keys('foo@example.com\n')
    self.get('#Password').send_keys('Password1')
    self.driver.hide_keyboard()
    self.get('Sign in', index=1).click()
    self.wait_until('Welcome')
    # self.dump_page()  <-- write the DOM to a file
    # self.repl()  <-- get an interactive shell
```

Here is an example test base class with those helpers:

```python
class AppiumTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723/wd/hub',
            desired_capabilities=OPTIONS)

    def tearDown(self):
        self.driver.quit()

    def repl(self):
        import pdb; pdb.set_trace()

      def dump_page(self):
          with open('appium_page.xml', 'w') as f:
              raw = self.driver.page_source
              if not raw:
                  return
              source = xml.dom.minidom.parseString(raw.encode('utf8'))
              f.write(source.toprettyxml())

    def _get(self, text, index=None, partial=False):
        ''' get RIGHT NOW, fail if it's not there '''
        selector = options['xpath_selector']
        if text.startswith('#'):
            elements = self.driver.find_elements_by_accessibility_id(text[1:])
        elif partial:
            elements = self.driver.find_elements_by_xpath('//*[contains(@%s, "%s")]' % (selector, text))
        else:
            elements = self.driver.find_elements_by_xpath('//*[@%s="%s"]' % (selector, text))
        if not elements:
            raise Exception()
        if index:
            return elements[index]
        if index is None and len(elements) > 1:
            raise IndexError('More that one element found for %r' % text)
        return elements[0]

    def get(self, text, *args, **kwargs):
        ''' try to get for X seconds; paper over loading waits/sleeps '''
        timeout_seconds = kwargs.get('timeout_seconds', 10)
        start = time.time()
        while time.time() - start < timeout_seconds:
            try:
                return self._get(text, *args, **kwargs)
            except IndexError:
                raise
            except:
                pass
            self.wait(.2)
        raise Exception('Could not find text %r after %r seconds' % (
            text, timeout_seconds))

    def wait_until(self, *args, **kwargs):
        # only care if there is at least one match
        return self.get(*args, index=0, **kwargs)
```
