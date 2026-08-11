# Stage 04: Converting Text to Whole Numbers

Stage 03 is mastered. Keyboard input, variables, reuse, reassignment, exact output, prompt text, and blank lines remain active knowledge and will keep returning.

## Current concept

`input()` returns text, and `int()` converts valid whole-number text into an integer.

Challenge 10 is the normal-drill capstone for Stage 04. It mixes a fixed header, one reused text slot, a preserved converted integer, a converted integer that is later reassigned, exact prompts, chosen output order, reuse, and a blank line. Arithmetic is still locked.

## Challenge 10: Conversion capstone

Create a fixed header containing exactly:

```text
[INTEGER CAPSTONE]
```

The first `input()` call must display exactly:

```text
First integer: 
```

When it waits, type exactly:

```text
31
```

Convert that keyboard text and preserve the integer separately.

The second `input()` call must display exactly:

```text
Current integer: 
```

When it waits, type exactly:

```text
58
```

Reuse the same text variable, convert the new text, and store that integer in a number variable.

Before taking the third input, print exactly:

```text
58
[INTEGER CAPSTONE]
31

```

Then the third `input()` call must display exactly:

```text
Next integer: 
```

When it waits, type exactly:

```text
76
```

Reuse the same text variable again. Convert the new text and reassign the same number variable that previously held the second converted integer.

After that third conversion, continue printing so the complete printed output is exactly:

```text
58
[INTEGER CAPSTONE]
31

[INTEGER CAPSTONE]
76
31
```

### Requirements

- Create exactly four variables named `header`, `text`, `first_number`, and `number`.
- Assign the exact string `[INTEGER CAPSTONE]` to `header` exactly once.
- Do not reassign `header`.
- Use `input()` exactly three times.
- The first `input()` call must contain the exact prompt string `First integer: ` and store its returned text in `text`.
- Use `int()` to convert that `text` and store the integer in `first_number`.
- The second `input()` call must contain the exact prompt string `Current integer: ` and reassign its returned text to `text`.
- Use `int()` to convert the new `text` and store the integer in `number`.
- Before the third `input()` call, print `number`, then `header`, then `first_number`, then create a blank output line.
- Only after those four `print()` calls, use the third `input()` call with the exact prompt string `Next integer: ` and reassign its returned text to `text`.
- Use `int()` again to convert the newest `text` and reassign the integer to the same `number` variable.
- After the third conversion, print `header`, then `number`, then `first_number`.
- Use `int()` exactly three times total.
- Use exactly seven `print()` calls total.
- Every non-blank `print()` call must print a variable.
- Do not print `text`.
- Do not write `31`, `58`, or `76` as numeric literals or string literals anywhere in your code.
- Do not create any additional variables.
- Do not use arithmetic yet.
- Use only variables, string literals, assignment with `=`, `input()`, `int()`, and `print()`.
- Type the code yourself.

### Submission

Write your attempt in [`work.py`](work.py), run it locally, commit it even if it is broken, then ask for review.

Only one challenge is unlocked at a time. After the normal-drill capstone is passed, Stage 04 will move to delayed recall checks before the stage can be mastered.
