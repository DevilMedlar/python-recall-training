# Challenge 13 — Division and float results

## Tiny lesson first

You already know that `input()` returns text and that `int()` converts suitable digit text into an integer.

Python uses `/` for division:

```python
items = 12
groups = 3
per_group = items / groups
print(per_group)
```

That prints:

```text
4.0
```

The important new distinction is that `/` produces a **float**, even when both operands are integers and the division comes out evenly. A float is a number that Python represents with a decimal point, such as `4.0` or `2.5`.

Important distinctions:

- `/` divides the value on the left by the value on the right.
- Division order matters.
- In Python, `/` returns a float.
- Do not wrap the division result in `int()` for this challenge.
- No new feature besides division with `/` and recognizing its float result is introduced here.

## Your task

Create this learner file yourself:

`stages/01-foundations/challenge_13.py`

Ask the user for a total number of items and a number of groups. Convert both answers to integers, divide the total-items integer by the number-of-groups integer, store the result, and print it.

Use these exact prompts:

```text
Total items: 
Number of groups: 
```

Example behavior: if the user enters `12` and then `3`, the program must print:

```text
4.0
```

### Requirements

1. Use exactly five variables total.
2. Use exactly two `input()` calls.
3. The first prompt must be exactly `Total items: ` including the trailing space.
4. The second prompt must be exactly `Number of groups: ` including the trailing space.
5. Store each `input()` result in its own variable before conversion.
6. Use exactly two `int()` calls.
7. Convert each stored input with `int()` and store each converted integer in a different variable.
8. Use the fifth variable to store the division result.
9. Divide the converted total-items variable by the converted number-of-groups variable with `/` exactly once.
10. Use exactly one `print()` call.
11. The `print()` call must print the variable containing the division result.
12. Use exactly two string literals total: the two required prompts.
13. Do not convert the division result to `int()` or any other type.
14. Do not reassign any variable.
15. Do not use `+`, `-`, `*`, concatenation, f-strings, or any other untaught feature.
16. Do not add extra output.
17. Type the program yourself rather than copying a completed passing solution.
18. Commit the learner file when finished and say `done`.
