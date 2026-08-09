# Stage 03: Keyboard Input as Text

Stage 02 is mastered. Variables, reassignment, exact output, quotation marks, and blank lines remain active knowledge and will keep returning.

## Current concept

Prompt text inside `input()` is displayed before Python waits for keyboard text. The returned keyboard text can still be stored and reused just like any other value you learned earlier.

Challenge 07 combines prompted input with reuse and an older blank-line skill. No new syntax is introduced.

## Challenge 07: Prompt, reuse, blank line

Run the program. The `input()` call must display exactly this prompt:

```text
Repeat: 
```

When it waits, type exactly:

```text
Prompted echo.
```

After you press Enter, the program must print exactly:

```text
Prompted echo.

Prompted echo.
```

### Requirements

- Create exactly one variable named `echo`.
- Use `input()` exactly once.
- Put the exact prompt string `Repeat: ` inside that `input()` call.
- Store the returned keyboard text in `echo`.
- Use exactly three `print()` calls.
- The first `print()` call must print `echo`.
- The second `print()` call must create the blank output line.
- The third `print()` call must print `echo` again.
- Do not write `Prompted echo.` as a string literal anywhere in your code.
- Do not create any additional variables.
- Use only variables, string literals, assignment with `=`, `input()`, and `print()`.
- Type the code yourself.

### Submission

Write your attempt in [`work.py`](work.py), run it locally, commit it even if it is broken, then ask for review.

Only one challenge is unlocked at a time. Prompted `input()` will continue mixing with earlier skills before delayed recall checks begin.
