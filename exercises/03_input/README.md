# Stage 03: Keyboard Input as Text

Stage 02 is mastered. Variables, reassignment, exact output, quotation marks, and blank lines remain active knowledge and will keep returning.

## New concept

`input()` pauses the program and waits for you to type something and press Enter.

The text you type is returned by `input()`. Because you already know assignment with `=`, that returned text can be stored in a variable and used later.

For this first drill, use `input()` with empty parentheses only. Do not put prompt text inside the parentheses yet.

## Challenge 01: Store keyboard text

Run the program and type exactly this when it waits for input:

```text
Memory came from me.
```

After you press Enter, the program must print exactly:

```text
Memory came from me.
```

### Requirements

- Create exactly one variable named `message`.
- Use `input()` exactly once.
- Assign the text returned by `input()` to `message`.
- Use exactly one `print()` call.
- The `print()` call must print `message`.
- Do not write `Memory came from me.` as a string literal anywhere in your code.
- Do not put any prompt text inside `input()` yet.
- Use only variables, assignment with `=`, `input()`, and `print()`.
- Type the code yourself.

### Submission

Write your attempt in [`work.py`](work.py), run it locally, commit it even if it is broken, then ask for review.

Only one challenge is unlocked at a time. `input()` will be repeated across multiple drills before another major concept appears.
