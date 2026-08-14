# Challenge 15 — Comparisons and booleans

## Tiny lesson first

Python comparisons ask questions about values and produce a boolean result.

A boolean is either:

```text
True
False
```

Three comparison operators are introduced here:

```python
first > second
first < second
first == second
```

They mean:

- `>` asks whether the left value is greater than the right value.
- `<` asks whether the left value is less than the right value.
- `==` asks whether the two values are equal.

Example:

```python
first = 8
second = 3
result = first > second
print(result)
```

That prints:

```text
True
```

Important distinction:

- `=` performs assignment.
- `==` performs an equality comparison.
- Comparison results are booleans, not strings. Do not put `True` or `False` in quotation marks.

For this challenge, comparisons with `>`, `<`, and `==`, plus boolean results, are the new Python ideas.

## Your task

Create this learner file yourself:

`stages/01-foundations/challenge_15.py`

Ask the user for two whole numbers, store each raw input separately, and convert both to integers.

Use these exact prompts:

```text
First integer: 
Second integer: 
```

Then use one result variable for all three comparisons in this exact sequence:

1. Compare whether the first integer is greater than the second integer and print the result.
2. Reassign the same result variable to whether the first integer is less than the second integer and print the result.
3. Reassign the same result variable to whether the two integers are equal and print the result.

Example behavior: if the user enters `7` and then `3`, the program must print:

```text
True
False
False
```

### Requirements

1. Use exactly five variables total.
2. Use exactly two `input()` calls.
3. The first prompt must be exactly `First integer: ` including the trailing space.
4. The second prompt must be exactly `Second integer: ` including the trailing space.
5. Store each `input()` result in its own variable before conversion.
6. Use exactly two `int()` calls.
7. Convert each stored input with `int()` and store each converted integer in a different variable.
8. Use the fifth variable as the result variable for all three comparisons.
9. First assign the result variable using `>` exactly once and print it.
10. Reassign that same result variable using `<` exactly once and print it.
11. Reassign that same result variable using `==` exactly once and print it.
12. Use exactly three `print()` calls, each printing the same result variable.
13. Use exactly two string literals total: the two required prompts.
14. Do not use arithmetic operators.
15. Do not write `True` or `False` directly in the program.
16. Do not reassign any variable except the result variable.
17. Do not use blank-line `print()` calls, concatenation, f-strings, `if`, or any other untaught feature.
18. Do not add extra output.
19. Type the program yourself rather than copying a completed passing solution.
20. Commit the learner file when finished and say `done`.
