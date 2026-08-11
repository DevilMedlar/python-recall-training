# Stage 04: Converting Text to Whole Numbers

Stage 03 is mastered. Keyboard input, variables, reuse, reassignment, exact output, and prompt text remain active knowledge and will keep returning.

## Current concept

`input()` returns text, and `int()` converts valid whole-number text into an integer.

Variables can be reassigned too. That means the same text variable can receive a later keyboard value, and the same number variable can receive the integer converted from that newer text.

Arithmetic is still locked. Challenge 04 combines conversion with reassignment using only two variables.

## Challenge 04: Reassign text, reassign number

The first `input()` call must display exactly:

```text
First number: 
```

When it waits, type exactly:

```text
21
```

Convert that keyboard text and print exactly:

```text
21
```

Then the second `input()` call must display exactly:

```text
Second number: 
```

When it waits, type exactly:

```text
88
```

Convert the new keyboard text and print exactly:

```text
88
```

### Requirements

- Create exactly two variables named `text` and `number`.
- Use `input()` exactly twice.
- The first `input()` call must contain the exact prompt string `First number: ` and store its returned text in `text`.
- Use `int()` to convert `text` and store the integer in `number`.
- Print `number`.
- Only after that first number has been printed, use a second `input()` call with the exact prompt string `Second number: ` and reassign its returned text to `text`.
- Use `int()` again to convert the new `text` and reassign the integer to `number`.
- Print `number` again.
- Use `int()` exactly twice total.
- Use exactly two `print()` calls total.
- Do not write `21` or `88` as numeric literals or string literals anywhere in your code.
- Do not create any additional variables.
- Do not use arithmetic yet.
- Use only variables, string literals, assignment with `=`, `input()`, `int()`, and `print()`.
- Type the code yourself.

### Submission

Write your attempt in [`work.py`](work.py), run it locally, commit it even if it is broken, then ask for review.

Only one challenge is unlocked at a time. Number conversion will keep repeating and mixing with earlier skills before arithmetic is introduced.
