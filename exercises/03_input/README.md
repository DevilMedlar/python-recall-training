# Stage 03: Keyboard Input as Text

Stage 02 is mastered. Variables, reassignment, exact output, quotation marks, and blank lines remain active knowledge and will keep returning.

## Current concept

`input()` waits for keyboard text and returns what you typed.

A variable that receives text from `input()` can be reassigned later, just like any other variable. The new keyboard value replaces the old stored value under that same name.

For now, keep using `input()` with empty parentheses only. Prompt text inside `input()` is still locked.

## Challenge 04: Reassign with keyboard input

Run the program. When it waits for input the first time, type exactly:

```text
First keyboard value.
```

After that value is printed, the program must wait for input again. Type exactly:

```text
Second keyboard value.
```

The program must print exactly:

```text
First keyboard value.
Second keyboard value.
```

### Requirements

- Create exactly one variable named `message`.
- Use `input()` exactly twice.
- Store the first keyboard value in `message`.
- Print `message` before the second `input()` call happens.
- Reassign the second keyboard value to that same `message` variable.
- Print `message` again after the reassignment.
- Use exactly two `print()` calls.
- Do not create a second variable.
- Do not write either keyboard value as a string literal anywhere in your code.
- Do not put prompt text inside either `input()` call.
- Use only variables, assignment with `=`, `input()`, and `print()`.
- Type the code yourself.

### Submission

Write your attempt in [`work.py`](work.py), run it locally, commit it even if it is broken, then ask for review.

Only one challenge is unlocked at a time. `input()` will keep repeating and mixing with older variable skills before another major concept appears.
