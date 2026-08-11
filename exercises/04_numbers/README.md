# Stage 04: Converting Text to Whole Numbers

Stage 03 is mastered. Keyboard input, variables, reuse, reassignment, exact output, prompt text, and blank lines remain active knowledge and will keep returning.

## Current concept

`input()` returns text, and `int()` converts valid whole-number text into an integer.

Challenge 08 keeps one text variable moving through two keyboard inputs while preserving both converted integers in separate number variables. Arithmetic is still locked.

## Challenge 08: Reuse the text slot, keep both numbers

Create a fixed tag containing exactly:

```text
[NUMBER PAIR]
```

The first `input()` call must display exactly:

```text
Left value: 
```

When it waits, type exactly:

```text
26
```

Convert that keyboard text and store the integer separately.

Then the second `input()` call must display exactly:

```text
Right value: 
```

When it waits, type exactly:

```text
84
```

Reuse the same text variable for this second keyboard value, convert it, and store the second integer separately.

After both conversions, print exactly:

```text
84
[NUMBER PAIR]
26

26
84
[NUMBER PAIR]
```

### Requirements

- Create exactly four variables named `tag`, `text`, `first_number`, and `second_number`.
- Assign the exact string `[NUMBER PAIR]` to `tag` exactly once.
- Do not reassign `tag`.
- Use `input()` exactly twice.
- The first `input()` call must contain the exact prompt string `Left value: ` and store its returned text in `text`.
- Use `int()` to convert `text` and store the integer in `first_number`.
- The second `input()` call must contain the exact prompt string `Right value: ` and reassign its returned text to the same `text` variable.
- Use `int()` again to convert the new `text` and store the integer in `second_number`.
- Use `int()` exactly twice total.
- Use exactly seven `print()` calls.
- Print `second_number`, then `tag`, then `first_number`.
- The fourth `print()` call must create the blank output line.
- Then print `first_number`, then `second_number`, then `tag`.
- Every non-blank `print()` call must print a variable.
- Do not print `text`.
- Do not write `26` or `84` as numeric literals or string literals anywhere in your code.
- Do not create any additional variables.
- Do not use arithmetic yet.
- Use only variables, string literals, assignment with `=`, `input()`, `int()`, and `print()`.
- Type the code yourself.

### Submission

Write your attempt in [`work.py`](work.py), run it locally, commit it even if it is broken, then ask for review.

Only one challenge is unlocked at a time. Number conversion will keep repeating and mixing with earlier skills before arithmetic is introduced.
