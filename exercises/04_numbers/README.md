# Stage 04: Converting Text to Whole Numbers

Stage 03 is mastered. Keyboard input, variables, reuse, reassignment, exact output, prompt text, and blank lines remain active knowledge and will keep returning.

## Current concept

`input()` returns text, and `int()` converts valid whole-number text into an integer.

Challenge 07 combines conversion with reassignment and a fixed tag. The same `text` and `number` variables will be reused for a second keyboard value while the tag remains unchanged.

Arithmetic is still locked.

## Challenge 07: Fixed tag with reassigned conversion

Create a fixed tag containing exactly:

```text
[NUMBER STATE]
```

The first `input()` call must display exactly:

```text
First integer: 
```

When it waits, type exactly:

```text
52
```

Convert that keyboard text into an integer, then print exactly:

```text
[NUMBER STATE]
52
```

Only after the first integer has been printed, the second `input()` call must display exactly:

```text
Second integer: 
```

When it waits, type exactly:

```text
91
```

Reassign the same text variable with that new keyboard text, convert it, and reassign the same number variable.

After the second conversion, continue printing so that the complete printed output is exactly:

```text
[NUMBER STATE]
52
91

[NUMBER STATE]
91
```

### Requirements

- Create exactly three variables named `tag`, `text`, and `number`.
- Assign the exact string `[NUMBER STATE]` to `tag` exactly once.
- Do not reassign `tag`.
- Use `input()` exactly twice.
- The first `input()` call must contain the exact prompt string `First integer: ` and store its returned text in `text`.
- Use `int()` to convert `text` and store the integer in `number`.
- Print `tag`, then `number`.
- Only after that first `number` has been printed, use the second `input()` call with the exact prompt string `Second integer: ` and reassign its returned text to `text`.
- Use `int()` again to convert the new `text` and reassign the integer to `number`.
- Then print `number`.
- The fourth `print()` call must create the blank output line.
- Then print `tag`, then `number` again.
- Use `int()` exactly twice total.
- Use exactly six `print()` calls total.
- Every non-blank `print()` call must print a variable.
- Do not write `52` or `91` as numeric literals or string literals anywhere in your code.
- Do not create any additional variables.
- Do not use arithmetic yet.
- Use only variables, string literals, assignment with `=`, `input()`, `int()`, and `print()`.
- Type the code yourself.

### Submission

Write your attempt in [`work.py`](work.py), run it locally, commit it even if it is broken, then ask for review.

Only one challenge is unlocked at a time. Number conversion will keep repeating and mixing with earlier skills before arithmetic is introduced.
