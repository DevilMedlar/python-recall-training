# Stage 03: Keyboard Input as Text

Stage 02 is mastered. Variables, reassignment, exact output, quotation marks, and blank lines remain active knowledge and will keep returning.

## Current concept

A variable can receive text from prompted `input()` more than once. Reassigning that variable changes only its stored value. Other variables keep their own values unless you reassign them too.

Challenge 08 mixes prompted input with an older Stage 02 pattern: one variable stays fixed while another variable changes.

## Challenge 08: One stays, prompted state changes

Create a fixed label and then collect two keyboard values in the same `state` variable.

The first `input()` call must display exactly this prompt:

```text
First state: 
```

When it waits, type exactly:

```text
Waiting.
```

After that input, print exactly:

```text
[INPUT STATUS]
Waiting.
```

Then the second `input()` call must display exactly this prompt:

```text
Second state: 
```

When it waits, type exactly:

```text
Ready.
```

After that input, print exactly:

```text
[INPUT STATUS]
Ready.
```

### Requirements

- Create exactly two variables named `label` and `state`.
- Assign the exact string `[INPUT STATUS]` to `label` exactly once.
- Use `input()` exactly twice.
- The first `input()` call must contain the exact prompt string `First state: ` and store the returned keyboard text in `state`.
- Print `label`, then print `state`.
- The second `input()` call must contain the exact prompt string `Second state: ` and reassign its returned keyboard text to the same `state` variable.
- Print `label` again, then print `state` again.
- Use exactly four `print()` calls.
- Every `print()` call must print a variable, not a string literal directly.
- Do not reassign `label`.
- Do not create any additional variables.
- Do not write `Waiting.` or `Ready.` as string literals anywhere in your code.
- Use only variables, string literals, assignment with `=`, `input()`, and `print()`.
- Type the code yourself.

### Submission

Write your attempt in [`work.py`](work.py), run it locally, commit it even if it is broken, then ask for review.

Only one challenge is unlocked at a time. Stage 03 will keep combining input with earlier skills before delayed recall checks begin.
