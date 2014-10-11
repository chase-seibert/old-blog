---
layout: post
title: My favorite coding interview question
tags: interview
---

Every software engineering interview I have ever participated in has involved a coding exercise. For one position, I
would expect three two five separate coding tests. I've [written previously](/blog/2012/08/31/how-to-prepare-for-a-software-engineer-interview.html)
about why every company asks these questions, and the best way to handle these as a candidate. But what makes a good coding question?

There is very little data out there about effective interviewing. What data does exists seems to suggest interviews are
only good for filtering out candidates that do not meet the minimum bar. According to one popular
[Google internal study](http://www.forbes.com/sites/quora/2013/06/28/is-there-a-link-between-job-interview-performance-and-job-performance/),
there is no correlation between interview results and on the job performance.

With this in mind, the coding question I ask is simple. I have found that you can hardly ask a question that's too
simple; a substantial number of candidates will have no problem hanging themselves with the smallest amount of rope
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
            current_char_seen = 0
            prev_char = current_char
        if current_char_seen < max_consecutive_chars:
            output += current_char
    return output
```

While the candidate is writing code, I focus on the following.

- Thought process. How do they get to a solution? Did they talk about their strategy?
- It needs to work. If it doesn't, I will keep pushing them until it does.
- Are the function and the variables well named?
- Is the code as simple as possible, but not more simple?
- Is the candidate struggling to remember standard library functions? Help them out.

## Other Solutions

The most common variant answer I see is conflating the clauses that count the character and append to the output. Typically this results in a bug where the last character in a run is omitted.

```python
def remove_extra_consecutive(input_str, max_consecutive_chars):
    output, prev_char, current_char_seen = '', None, 1
    for current_char in input_str:
        if current_char == prev_char and current_char_seen < max_consecutive_chars:
            current_char_seen += 1
            output += current_char
        else:
            if current_char != prev_char:
                current_char_seen = 1
                output += current_char
        prev_char = current_char
    return output
```

Another variant is using indexes instead of a named variable for the previous character. This can often lead to an index out of bounds bug. It's also common to forget to add the last character.

```python
def remove_extra_consecutive(input_str, max_consecutive_chars):
    output, current_char_seen = '', 0
    for i in range(len(input_str) - 1):
        if input_str[i] == input_str[i+1]:
            current_char_seen += 1
        else:
            current_char_seen = 0
        if current_char_seen < max_consecutive_chars:
            output += input_str[i]
    if current_char_seen <= max_consecutive_chars:
        output += input_str[i+1]
    return output
```

Finally some candidates try to alter the input string itself, or sometimes loop indexes, which can lead of off by one errors.

```python
def remove_extra_consecutive(str, max_consecutive_chars):
    for i in range(len(str)):
        j = i + 1
        while j < len(str):
            if str[i] != str[j]:
                break
            if j - i >= max_consecutive_chars:
                str = str[0:j] + str[j+1:]
            j += 1
    return str
```

## Summary

I like this problem because it has one simple and robust solution, and a number of more complicated and brittle solutions. If a candidate gets through it quickly and correctly, I follow up by asking them about which edge cases they would want to create unit tests for. If it's in a dynamic language, I ask about how to make the function operate on any iterable.
