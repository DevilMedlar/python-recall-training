# Stage 03: Keyboard Input as Text

Stage 02 is mastered. Variables, reassignment, exact output, quotation marks, and blank lines remain active knowledge and will keep returning.

## Current concept

`input()` can display prompt text and return only what the user types.

Different prompted `input()` calls can store different keyboard values in separate variables. Those stored values can then be printed in any order, just like variables from Stage 02.

## Challenge 06: Two prompts, reverse output

Run the program. The first `input()` call must display exactly this prompt:

```text
First: 
```

When it waits, type exactly:

```text
Keyboard one.
```

The second `input()` call must display exactly this prompt:

```text
Second: 
```

When it waits, type exactly:

```text
Keyboard two.
```

After both inputs have been entered, the program must print exactly:

```text
Keyboard two.
Keyboard one.
```

### Requirements

- Create exactly two variables named `first_text` and `second_text`.
- Use `input()` exactly twice.
- The first `input()` call must contain the exact prompt string `First: ` and store the returned keyboard text in `first_text`.
- The second `input()` call must contain the exact prompt string `Second: ` and store the returned keyboard text in `second_text`.
- Use exactly two `print()` calls.
- First print `second_text`.
- Then print `first_text`.
- Do not write either keyboard value as a string literal anywhere in your code.
- Do not create any additional variables.
- Use only variables, string literals, assignment with `=`, `input()`, and `print()`.
- Type the code yourself.

### Submission

Write your attempt in [`work.py`](work.py), run it locally, commit it even if it is broken, then ask for review.

Only one challenge is unlocked at a time. Prompted `input()` will keep repeating and mixing with earlier skills before another major concept appears.
