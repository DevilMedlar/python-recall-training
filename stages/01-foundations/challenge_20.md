# Challenge 20 — `break` and `continue`

## Tiny lesson first

You now know two ways to repeat code: `while` repeats while a condition stays true, and `for` takes values from a sequence such as `range()`.

Two statements can change what happens inside a loop:

- `continue` skips the rest of the **current iteration** and moves to the next iteration.
- `break` exits the **entire current loop** immediately.

Example:

```python
for number in range(1, 7):
    if number == 2:
        continue
    if number == 5:
        break
    print(number)
```

That prints:

```text
1
3
4
```

Why:

- `1` prints normally.
- At `2`, `continue` skips the print for that iteration.
- `3` and `4` print normally.
- At `5`, `break` ends the loop completely, so `5` is not printed and `6` is never reached.

For this challenge, `break` and `continue` are the new Python statements. `for`, `range()`, `if`, `==`, indentation, and `print()` are already unlocked.

## Your task

Create this learner file yourself:

`stages/01-foundations/challenge_20.py`

Use one `for` loop with `range(1, 9)`.

Inside the loop:

- when the loop variable equals `3`, use `continue`
- when the loop variable equals `7`, use `break`
- otherwise print the loop variable

The program must output:

```text
1
2
4
5
6
```

### Requirements

1. Use exactly one variable total: the loop variable.
2. Use exactly one `for` loop.
3. Use exactly one `range()` call with exactly two arguments: `1` and `9`.
4. End the `for` line with a colon.
5. Inside the loop, use exactly two `if` statements.
6. The first `if` must compare the loop variable to `3` using `==`.
7. The first `if` body must contain exactly one `continue` statement.
8. The second `if` must compare the loop variable to `7` using `==`.
9. The second `if` body must contain exactly one `break` statement.
10. After both `if` statements, still inside the `for` loop, use exactly one `print()` call that prints the loop variable.
11. Use exactly one `continue` in the entire program.
12. Use exactly one `break` in the entire program.
13. Use exactly one `print()` call in the source code.
14. Use exactly four integer literal values in the source code: `1`, `9`, `3`, and `7`.
15. Use no string literals.
16. Do not use `while`, `elif`, `else`, arithmetic operators, other comparison operators, boolean literals, nested loops, or any other untaught feature.
17. Do not manually reassign the loop variable.
18. Do not add extra output.
19. Type the program yourself rather than copying a completed passing solution.
20. Commit the learner file when finished and say `done`.
