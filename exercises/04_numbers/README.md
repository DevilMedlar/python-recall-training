# Stage 04: Converting Text to Whole Numbers

Stage 03 is mastered. Keyboard input, variables, reuse, reassignment, exact output, and prompt text remain active knowledge and will keep returning.

## Current concept

`input()` returns text, and `int()` converts valid whole-number text into an integer.

Converted integers can be stored and reused alongside ordinary text variables. Challenge 05 mixes number conversion with an older fixed-label, reuse, and blank-line pattern.

Arithmetic is still locked.

## Challenge 05: Fixed label, converted number, reuse

Create a fixed label containing exactly:

```text
[NUMBER MEMORY]
```

Then the `input()` call must display exactly:

```text
Value: 
```

When it waits, type exactly:

```text
37
```

Convert the keyboard text into an integer.

The five `print()` calls must produce exactly:

```text
[NUMBER MEMORY]
37

37
[NUMBER MEMORY]
```

### Requirements

- Create exactly three variables named `label`, `text`, and `number`.
- Assign the exact string `[NUMBER MEMORY]` to `label` exactly once.
- Do not reassign `label`.
- Use `input()` exactly once.
- Put the exact prompt string `Value: ` inside the `input()` call.
- Store the returned keyboard text in `text`.
- Use `int()` exactly once to convert `text`.
- Store the converted integer in `number`.
- Use exactly five `print()` calls.
- Print `label`, then `number`.
- The third `print()` call must create the blank output line.
- Then print `number`, then `label` again.
- Every non-blank `print()` call must print a variable.
- Do not print `text`.
- Do not write `37` as either a numeric literal or a string literal anywhere in your code.
- Do not create any additional variables.
- Do not use arithmetic yet.
- Use only variables, string literals, assignment with `=`, `input()`, `int()`, and `print()`.
- Type the code yourself.

### Submission

Write your attempt in [`work.py`](work.py), run it locally, commit it even if it is broken, then ask for review.

Only one challenge is unlocked at a time. Number conversion will keep repeating and mixing with earlier skills before arithmetic is introduced.
