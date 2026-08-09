# Stage 03: Keyboard Input as Text

Stage 02 is mastered. Variables, reassignment, exact output, quotation marks, and blank lines remain active knowledge and will keep returning.

## New concept

So far, `input()` has used empty parentheses and waited silently.

A string literal can also go inside the parentheses:

```python
input("Prompt text: ")
```

Python displays that prompt text first, then waits for keyboard input. The value returned by `input()` is still only the text you type. The prompt itself is not stored as part of that returned value.

## Challenge 05: Prompt, store, print

Run the program. Before it waits for input, it must display exactly this prompt:

```text
Type this: 
```

The prompt must end with one space after the colon so the keyboard text begins on the same line with a gap.

When it waits for input, type exactly:

```text
Prompt remembered.
```

After you press Enter, the program must print exactly:

```text
Prompt remembered.
```

### Requirements

- Create exactly one variable named `message`.
- Use `input()` exactly once.
- Put the exact string literal `Type this: ` inside that `input()` call.
- Assign the text returned by `input()` to `message`.
- Use exactly one `print()` call.
- The `print()` call must print `message`.
- Do not write `Prompt remembered.` as a string literal anywhere in your code.
- Do not create any additional variables.
- Use only variables, string literals, assignment with `=`, `input()`, and `print()`.
- Type the code yourself.

### Submission

Write your attempt in [`work.py`](work.py), run it locally, commit it even if it is broken, then ask for review.

Only one challenge is unlocked at a time. Prompted `input()` will be repeated and mixed with earlier skills before another major concept appears.
