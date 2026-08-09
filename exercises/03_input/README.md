# Stage 03: Keyboard Input as Text

Stage 02 is mastered. Variables, reassignment, exact output, quotation marks, and blank lines remain active knowledge and will keep returning.

## Current concept

`input()` waits for keyboard text and returns what you typed.

That returned text can be stored in a variable. Different `input()` calls can store different pieces of text in different variables, and those variables can be printed in any order.

For now, keep using `input()` with empty parentheses only. Prompt text inside `input()` is still locked.

## Challenge 02: Two inputs, reverse output

Run the program. When it waits for input the first time, type exactly:

```text
First keyboard line.
```

When it waits for input the second time, type exactly:

```text
Second keyboard line.
```

After both inputs have been entered, the program must print exactly:

```text
Second keyboard line.
First keyboard line.
```

### Requirements

- Create exactly two variables named `first_message` and `second_message`.
- Use `input()` exactly twice.
- Store the first keyboard value in `first_message`.
- Store the second keyboard value in `second_message`.
- Use exactly two `print()` calls.
- First print `second_message`.
- Then print `first_message`.
- Do not write either keyboard line as a string literal anywhere in your code.
- Do not put prompt text inside either `input()` call.
- Use only variables, assignment with `=`, `input()`, and `print()`.
- Type the code yourself.

### Submission

Write your attempt in [`work.py`](work.py), run it locally, commit it even if it is broken, then ask for review.

Only one challenge is unlocked at a time. `input()` will be repeated and mixed with older variable skills before another major concept appears.
