# Stage 04: Converting Text to Whole Numbers

Stage 03 is mastered. Keyboard input, variables, reuse, reassignment, exact output, and prompt text remain active knowledge and will keep returning.

## New concept

`input()` always returns text, even when the user types digits.

`int()` can convert text that represents a whole number into an integer value. For example, `int("42")` produces the integer `42`.

For now, enter only valid whole-number text when a challenge asks for it. Arithmetic is still locked. The goal of this stage begins with understanding the conversion itself.

## Challenge 01: Text first, number second

Run the program. It must display exactly this prompt:

```text
Whole number: 
```

When it waits, type exactly:

```text
42
```

After you press Enter, the program must print exactly:

```text
42
```

### Requirements

- Create exactly two variables named `text` and `number`.
- Use `input()` exactly once.
- Put the exact prompt string `Whole number: ` inside the `input()` call.
- Store the text returned by `input()` in `text`.
- Use `int()` exactly once to convert `text` to a whole-number integer.
- Store that converted integer in `number`.
- Use exactly one `print()` call.
- The `print()` call must print `number`.
- Do not write `42` as either a numeric literal or a string literal anywhere in your code.
- Do not create any additional variables.
- Do not use arithmetic yet.
- Use only variables, string literals, assignment with `=`, `input()`, `int()`, and `print()`.
- Type the code yourself.

### Submission

Write your attempt in [`work.py`](work.py), run it locally, commit it even if it is broken, then ask for review.

Only one challenge is unlocked at a time. Number conversion will repeat and mix with earlier skills before arithmetic is introduced.
