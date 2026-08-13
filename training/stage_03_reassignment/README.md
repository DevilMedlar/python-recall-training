# Stage 03 - Reassignment

## Goal

Learn that a variable can be assigned a new value later, and that later code uses the newest value.

## Tiny lesson

A variable name can refer to one value, then be assigned again:

```python
status = "waiting"
status = "ready"
print(status)
```

The output is:

```text
ready
```

The second assignment changes what `status` refers to from that point forward. Python executes the statements from top to bottom, so `print(status)` uses the most recent assignment.

For this challenge, use only what has already been taught: `print()`, quoted string literals, variables, assignment, and reassignment.

## Challenge 01

Write the solution yourself in `learner.py`.

### Requirements

1. Create a variable named `mood`.
2. First assign `mood` the string `Calm`.
3. Use one `print()` call to print `mood` while it still contains `Calm`.
4. Reassign the same variable `mood` to the string `Focused`.
5. Use a second `print()` call to print `mood` after the reassignment.
6. Use exactly two `print()` calls total.
7. Do not create any other variables.
8. Do not use `input()`.
9. Do not repeat either required string literal directly inside `print()`.
10. Do not add extra output.
11. Type the Python yourself from memory.

## Required output

```text
Calm
Focused
```

Commit your attempt, then tell Senpai `done`.
