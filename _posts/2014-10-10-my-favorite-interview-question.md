---
layout: post
title: My favorite coding interview question
tags: interview
---

Every software engineering interview I have ever participated in has involved a coding exercise. For one position, I
would expect three two five separate coding tests. I've [written previously](http://localhost:4000/blog/2012/08/31/how-to-prepare-for-a-software-engineer-interview.html)
about why every company asks these questions, and the best way to handle these as a candidate. But what makes a good
coding question, or a good interview question for that matter?

There is very little data out there about effective interviewing. What data does exists seems to suggest interviews are
only good for filtering out candidates that do not meet the minimum bar. According to one popular
[Google internal study](http://www.forbes.com/sites/quora/2013/06/28/is-there-a-link-between-job-interview-performance-and-job-performance/),
there is no correlation between interview results and on the job performance.

With this in mind, the coding question I ask is simple. I have found that you can hardly ask a question that's too
simple; a substantial number of candidates will have no problem handing themselves with the smallest amount of rope
that you can give them.

## The Question

>Write a function that takes two parameters, a string and an integer. The function will return another string that
>is similar to the input string, but with certain characters removed. It's going to remove characters from consecutive
>runs of the same character, where the length of the run is greater than the input parameter.

    Ex: "aaab", 2 => "aab"
    Ex: "aabb", 1 => "ab"
    Ex: "aabbaa", 1 => "aba"

*Note: I'm evaluating your answer on the simplicity of your code. The goal is for it to be readable; someone new
should be able to walk into this room afterwards and instantly understand what your function is doing.*

## The Evaluation

I explicitly state the part about what I'm looking for with the candidate. I tell them to use the language they are
most comfortable with. Here is what I consider an ideal solution, in Python:

```python
def remove_extra_consecutive(input_str, max_consecutive_chars):
    output, prev_char, current_char_seen = '', None, 0
    for current_char in input_str:
        if current_char == prev_char:
            current_char_seen += 1
        else:
            current_char = 0
        if current_char < max_consecutive_chars:
            output += current_char
     return output
```

- Your thought process. How did you get to a solution? Did you talk about your strategy?
- It needs to work. If it doesn't, I will keep pushing you until it does.
- Don't remember the standard library syntax? No problem, just ask. This is not a memory test.
- Are the function and the variables well named? I want to see descriptive names to aid the reader, no single letter names.
- Was your code an simple as possible, but not more simple? I'm not looking for the least number of lines of code.

## Other Solutions
