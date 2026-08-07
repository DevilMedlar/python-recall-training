# Stage 02: Variables That Store Text

Stage 01 is complete. `print()` remains active knowledge and will keep appearing while you learn variables.

## Current concept

Reassigning one variable changes only the value stored under that variable name. Other variables keep their own values unless you reassign them too.

Python still runs from top to bottom, so a variable can stay unchanged while another variable changes around it.

## Challenge 09: One changes, one stays

Write a Python program that produces exactly this output:

```text
[STATUS]
Waiting.
[STATUS]
Running.
```

### Requirements

- Create exactly two variables named `label` and `state`.
- Assign `[STATUS]` to `label` exactly once.
- First assign `Waiting.` to `state`.
- Print `label`, then print `state`.
- Reassign `Running.` to the same `state` variable.
- Print `label` again, then print `state` again.
- Use exactly four `print()` calls.
- Every `print()` call must print a variable, not a string literal directly.
- Do not reassign `label`.
- Do not create any additional variables.
- Use only variables, string literals, assignment with `=`, and `print()`.
- Type the code yourself.

### Submission

Write your attempt in [`work.py`](work.py), commit it even if it is broken, then ask for review.

Only one challenge is unlocked at a time. Stage 02 will continue mixing assignment, reuse, reassignment, and older `print()` skills before delayed recall checks begin.
