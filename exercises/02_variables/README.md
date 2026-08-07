# Stage 02: Variables That Store Text

Stage 01 is complete. `print()` remains active knowledge and will keep appearing while you learn variables.

## Current concept

Variables can be assigned, reused, printed in any order, and reassigned later. Each `print()` call uses the value a variable stores at that exact point in the program.

Challenge 10 combines the Stage 02 skills without introducing new syntax.

## Challenge 10: Variable capstone

Write a Python program that produces exactly this output:

```text
She said, "Keep the name."
[VARIABLE CAPSTONE]
Waiting.

[VARIABLE CAPSTONE]
Running.
She said, "Keep the name."
```

### Requirements

- Create exactly three variables named `header`, `message`, and `state`.
- Assign `[VARIABLE CAPSTONE]` to `header` exactly once.
- Assign `She said, "Keep the name."` to `message` exactly once.
- First assign `Waiting.` to `state`.
- Reassign `Running.` to the same `state` variable only after the first `Waiting.` output has been printed.
- Use exactly seven `print()` calls, including the call that produces the blank fourth output line.
- Every non-blank `print()` call must print a variable, not a repeated string literal.
- Print the variables in whatever order is necessary to match the required output exactly.
- Do not reassign `header` or `message`.
- Do not create any additional variables.
- Use only variables, string literals, assignment with `=`, and `print()`.
- Type the code yourself.

### Submission

Write your attempt in [`work.py`](work.py), commit it even if it is broken, then ask for review.

This is the final normal drill in Stage 02. Passing it completes the drill set, but delayed recall checks will still be required before Stage 02 is mastered and another major Python feature is introduced.
