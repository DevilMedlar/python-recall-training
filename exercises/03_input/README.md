# Stage 03: Keyboard Input as Text

Stage 02 is mastered. Variables, reassignment, exact output, quotation marks, and blank lines remain active knowledge and will keep returning.

## Current concept

`input()` waits for keyboard text and returns what you typed.

Once that returned text is stored in a variable, the variable can be reused just like any other stored text value you already learned in Stage 02.

For now, keep using `input()` with empty parentheses only. Prompt text inside `input()` is still locked.

## Challenge 03: Input, reuse, blank line

Run the program. When it waits for input, type exactly:

```text
Echo from keyboard.
```

After you press Enter, the program must print exactly:

```text
Echo from keyboard.

Echo from keyboard.
```

### Requirements

- Create exactly one variable named `echo`.
- Use `input()` exactly once.
- Store the keyboard value in `echo`.
- Use exactly three `print()` calls.
- The first `print()` call must print `echo`.
- The second `print()` call must create the blank output line.
- The third `print()` call must print `echo` again.
- Do not write `Echo from keyboard.` as a string literal anywhere in your code.
- Do not put prompt text inside `input()`.
- Use only variables, assignment with `=`, `input()`, and `print()`.
- Type the code yourself.

### Submission

Write your attempt in [`work.py`](work.py), run it locally, commit it even if it is broken, then ask for review.

Only one challenge is unlocked at a time. `input()` will keep repeating and mixing with older skills before another major concept appears.
