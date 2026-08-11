# Stage 04: Converting Text to Whole Numbers

Stage 03 is mastered. Keyboard input, variables, reuse, reassignment, exact output, and prompt text remain active knowledge and will keep returning.

## Current concept

`input()` always returns text, even when the user types digits.

`int()` converts valid whole-number text into an integer. Once converted, that integer can be stored and reused just like other values you have already practiced.

Arithmetic is still locked. Challenge 03 mixes integer conversion with an older reuse-and-blank-line pattern.

## Challenge 03: Convert once, reuse twice

Run the program. The `input()` call must display exactly:

```text
Number: 
```

When it waits, type exactly:

```text
64
```

After the value has been entered and converted, the program must print exactly:

```text
64

64
```

### Requirements

- Create exactly two variables named `text` and `number`.
- Use `input()` exactly once.
- Put the exact prompt string `Number: ` inside the `input()` call.
- Store the returned keyboard text in `text`.
- Use `int()` exactly once to convert `text`.
- Store the converted integer in `number`.
- Use exactly three `print()` calls.
- The first `print()` call must print `number`.
- The second `print()` call must create the blank output line.
- The third `print()` call must print `number` again.
- Do not print `text`.
- Do not write `64` as either a numeric literal or a string literal anywhere in your code.
- Do not create any additional variables.
- Do not use arithmetic yet.
- Use only variables, string literals, assignment with `=`, `input()`, `int()`, and `print()`.
- Type the code yourself.

### Submission

Write your attempt in [`work.py`](work.py), run it locally, commit it even if it is broken, then ask for review.

Only one challenge is unlocked at a time. Number conversion will keep repeating and mixing with earlier skills before arithmetic is introduced.
