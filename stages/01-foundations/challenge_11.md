# Challenge 11 — Integer subtraction

## Tiny lesson first

You already know that `input()` returns text and that `int()` can convert suitable digit text into an integer.

Integers can also be subtracted with `-`:

```python
start = 10
used = 3
remaining = start - used
print(remaining)
```

That prints:

```text
7
```

Subtraction is order-sensitive. `10 - 3` is `7`, while `3 - 10` is `-7`.

Important distinctions:

- `-` subtracts the value on the right from the value on the left.
- The order of the operands matters.
- The result of integer subtraction is an integer.
- A variable can store the subtraction result.
- No new feature besides integer subtraction with `-` is introduced here.

## Your task

Create this learner file yourself:

`stages/01-foundations/challenge_11.py`

Ask the user for a starting amount and an amount used. Convert both answers to integers, subtract the amount used from the starting amount, and print the result.

Use these exact prompts:

```text
Starting amount: 
Amount used: 
```

Example behavior: if the user enters `12` and then `5`, the program must print:

```text
7
```

### Requirements

1. Use exactly five variables total.
2. Use exactly two `input()` calls.
3. The first prompt must be exactly `Starting amount: ` including the trailing space.
4. The second prompt must be exactly `Amount used: ` including the trailing space.
5. Store each `input()` result in its own variable before conversion.
6. Use exactly two `int()` calls.
7. Convert each stored input with `int()` and store each converted integer in a different variable.
8. Use the fifth variable to store the subtraction result.
9. Subtract the converted amount-used variable from the converted starting-amount variable with `-` exactly once.
10. Use exactly one `print()` call.
11. The `print()` call must print the variable containing the subtraction result.
12. Use exactly two string literals total: the two required prompts.
13. Do not reassign any variable.
14. Do not use `+`, multiplication, division, concatenation, f-strings, or any other untaught feature.
15. Do not add extra output.
16. Type the program yourself rather than copying a completed passing solution.
17. Commit the learner file when finished and say `done`.
