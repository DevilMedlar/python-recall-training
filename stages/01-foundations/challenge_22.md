# Challenge 22 — string methods: `.upper()` and `.lower()`

## Tiny lesson first

Strings have methods: operations you call on a string value using a dot.

Example:

```python
text = "Python"
upper_text = text.upper()
lower_text = text.lower()
```

`.upper()` returns a new string with letters converted to uppercase.

`.lower()` returns a new string with letters converted to lowercase.

Important mental model:

- The dot connects a value to one of its methods.
- The parentheses call the method.
- These methods return new strings.
- They do not automatically replace the original variable unless you explicitly assign the returned value back to it.

For this challenge, method-call dot syntax, `.upper()`, and `.lower()` are the new Python ideas.

## Your task

Create this learner file yourself:

`stages/01-foundations/challenge_22.py`

Ask the user for text with this exact prompt:

```text
Type text: 
```

Store the entered text in one variable.

Create a second variable containing the uppercase version of that stored text using `.upper()`.

Create a third variable containing the lowercase version of the original stored text using `.lower()`.

Then print, in this exact order:

1. the original stored text
2. the uppercase version
3. the lowercase version

### Requirements

1. Use exactly three variables total: one original-text variable, one uppercase-result variable, and one lowercase-result variable.
2. Use exactly one `input()` call with the prompt `Type text: ` including the trailing space.
3. Store the raw text returned by `input()` in the first variable.
4. Use exactly one `.upper()` call.
5. Call `.upper()` on the original-text variable and store the returned string in the second variable.
6. Use exactly one `.lower()` call.
7. Call `.lower()` on the original-text variable and store the returned string in the third variable.
8. Do not reassign any of the three variables.
9. Use exactly three `print()` calls.
10. The first `print()` must print the original-text variable.
11. The second `print()` must print the uppercase-result variable.
12. The third `print()` must print the lowercase-result variable.
13. Use exactly one string literal in the source code: the `Type text: ` prompt.
14. Do not use `int()`, arithmetic operators, comparison operators, `if`, `elif`, `else`, `for`, `while`, `range()`, `break`, `continue`, or any other untaught feature.
15. Do not add extra output.
16. Type the program yourself rather than copying a completed passing solution.
17. Commit the learner file when finished and say `done`.
