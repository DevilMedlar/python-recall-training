# Challenge 16 — `if` and `else`

## Tiny lesson first

A comparison produces a boolean result such as `True` or `False`.

An `if` statement uses that result to decide whether an indented block of code runs:

```python
number = 12
if number > 10:
    print("Above 10.")
```

Because `12 > 10` is `True`, the indented `print()` runs.

An `else` block runs when the `if` condition is `False`:

```python
number = 4
if number > 10:
    print("Above 10.")
else:
    print("10 or below.")
```

That prints:

```text
10 or below.
```

Important distinctions:

- `if` is followed by a condition and a colon `:`.
- The code controlled by `if` must be indented.
- `else` also ends with a colon `:`.
- The code controlled by `else` must be indented.
- Exactly one of these two branches runs for a simple `if`/`else` pair.
- The comparison still produces the boolean result. `if` simply uses that result to choose a branch.

For this challenge, `if`, `else`, colons, and indentation-based branching are the new Python ideas.

## Your task

Create this learner file yourself:

`stages/01-foundations/challenge_16.py`

Ask the user for one whole number, store the raw input, and convert it to an integer.

Use this exact prompt:

```text
Enter an integer: 
```

Then:

- if the integer is greater than `10`, print exactly `Above 10.`
- otherwise, print exactly `10 or below.`

### Requirements

1. Use exactly two variables total.
2. Use exactly one `input()` call.
3. The prompt must be exactly `Enter an integer: ` including the trailing space.
4. Store the `input()` result in one variable before conversion.
5. Use exactly one `int()` call.
6. Store the converted integer in the second variable.
7. Use exactly one `if` statement.
8. The `if` condition must compare the converted integer variable to the integer literal `10` using `>` exactly once.
9. End the `if` line with a colon.
10. Indent the `print()` controlled by the `if` block.
11. Use exactly one `else` block paired with that `if`.
12. End the `else` line with a colon.
13. Indent the `print()` controlled by the `else` block.
14. Use exactly two `print()` calls total, one in each branch.
15. The `if` branch must print exactly `Above 10.`
16. The `else` branch must print exactly `10 or below.`
17. Use exactly three string literals total: the prompt and the two required output strings.
18. Use exactly one integer literal in the entire program: `10`.
19. Do not use `<`, `==`, arithmetic operators, boolean literals, additional comparisons, nested conditions, or any other untaught feature.
20. Do not add extra output.
21. Type the program yourself rather than copying a completed passing solution.
22. Commit the learner file when finished and say `done`.
