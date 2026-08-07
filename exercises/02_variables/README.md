# Stage 02: Variables That Store Text

Stage 01 is complete. `print()` remains active knowledge and will keep appearing while you learn variables.

## Current concept

A variable gives a value a name so you can use that value later.

You already know that a variable can be reused and printed in any order. Now add one more behavior: **a variable can be assigned a new value later**.

Example:

```python
mode = "Day"
print(mode)
mode = "Night"
print(mode)
```

After the second assignment, `mode` no longer stores `Day`. It now stores `Night`.

Important details:

- Reassignment uses the same `=` you already know.
- You do not need a new variable just because the value changes.
- A `print()` call uses whatever value the variable stores at that moment.
- Python still runs the file from top to bottom.

## Challenge 07: Change what one variable stores

Write a Python program that produces exactly this output:

```text
Loading...
Ready.
```

### Requirements

- Create exactly one variable named `status`.
- First assign `Loading...` to `status`.
- Print `status`.
- Then assign `Ready.` to that same `status` variable.
- Print `status` again.
- Use exactly two `print()` calls.
- Both `print()` calls must print the variable, not string literals directly.
- Do not create a second variable.
- Use only variables, string literals, assignment with `=`, and `print()`.
- Type the code yourself.

### Submission

Write your attempt in [`work.py`](work.py), commit it even if it is broken, then ask for review.

Only one challenge is unlocked at a time. Variables will keep repeating before another major Python feature is introduced.
