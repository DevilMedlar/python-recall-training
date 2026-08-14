# Challenge 09 — Integer conversion and addition

## Tiny lesson first

`input()` returns text. If the user types digits such as `12`, the value returned by `input()` is still text until you convert it.

`int()` converts suitable digit text into an integer:

```python
number_text = input("Number: ")
number = int(number_text)
```

If the user typed `12`, `number_text` refers to the text `"12"`, while `number` refers to the integer `12`.

Integers can be added with `+`:

```python
first = 4
second = 3
total = first + second
print(total)
```

That prints:

```text
7
```

Important distinctions:

- `input()` returns text.
- `int(...)` converts suitable text to an integer.
- Integer literals such as `4` are written without quotation marks.
- `+` adds integer values.
- A variable can store the result of an addition.
- Do not use string concatenation for this challenge.

For this challenge, `int()`, integer values, and integer addition with `+` are the new Python ideas.

## Your task

Create this learner file yourself:

`stages/01-foundations/challenge_09.py`

Ask the user for two whole numbers, convert both answers to integers, add them, then print one blank line followed by the sum.

Use these exact prompts:

```text
First number: 
Second number: 
```

Example behavior: if the user enters `7` and then `5`, the final printed result after the blank line must be:

```text
12
```

### Requirements

1. Use exactly five variables total.
2. Use exactly two `input()` calls.
3. The first prompt must be exactly `First number: ` including the trailing space.
4. The second prompt must be exactly `Second number: ` including the trailing space.
5. Store each `input()` result in its own variable before conversion.
6. Use exactly two `int()` calls.
7. Convert each stored input value with `int()` and store each converted integer in a different variable.
8. Add the two converted integer variables with `+` exactly once.
9. Store the addition result in the fifth variable.
10. Use exactly two `print()` calls.
11. The first `print()` call must be an empty `print()` that creates one blank line after the calculations.
12. The second `print()` call must print the variable containing the sum.
13. Use exactly two string literals total: the two required input prompts.
14. Do not reassign any variable.
15. Do not use concatenation, f-strings, arithmetic other than the one required `+`, or any other untaught feature.
16. Do not add extra output.
17. Type the program yourself rather than copying a completed passing solution.
18. Commit the learner file when finished and say `done`.
