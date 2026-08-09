# Stage 03: Keyboard Input as Text

Stage 02 is mastered. Variables, reassignment, exact output, quotation marks, and blank lines remain active knowledge and will keep returning.

## Current concept

Prompted `input()` can collect multiple separate keyboard values. Those values can be stored in different variables, reused later, and printed in any order.

Challenge 09 mixes that with earlier skills: one fixed stored label, two prompted keyboard values, reuse, chosen output order, and a blank line. No new syntax is introduced.

## Challenge 09: Two inputs, fixed label, mixed output

Create a fixed label and collect two keyboard values in separate variables.

The first `input()` call must display exactly this prompt:

```text
First line: 
```

When it waits, type exactly:

```text
Keyboard alpha.
```

The second `input()` call must display exactly this prompt:

```text
Second line: 
```

When it waits, type exactly:

```text
Keyboard beta.
```

After both inputs have been entered, the program must print exactly:

```text
[INPUT MEMORY]
Keyboard beta.

Keyboard alpha.
[INPUT MEMORY]
Keyboard beta.
```

### Requirements

- Create exactly three variables named `header`, `first_line`, and `second_line`.
- Assign the exact string `[INPUT MEMORY]` to `header` exactly once.
- Use `input()` exactly twice.
- The first `input()` call must contain the exact prompt string `First line: ` and store the returned keyboard text in `first_line`.
- The second `input()` call must contain the exact prompt string `Second line: ` and store the returned keyboard text in `second_line`.
- Use exactly six `print()` calls.
- Print `header`, then `second_line`.
- The third `print()` call must create the blank output line.
- Then print `first_line`, `header`, and `second_line` in that order.
- Every non-blank `print()` call must print a variable, not a string literal directly.
- Do not reassign any variable.
- Do not create any additional variables.
- Do not write `Keyboard alpha.` or `Keyboard beta.` as string literals anywhere in your code.
- Use only variables, string literals, assignment with `=`, `input()`, and `print()`.
- Type the code yourself.

### Submission

Write your attempt in [`work.py`](work.py), run it locally, commit it even if it is broken, then ask for review.

Only one challenge is unlocked at a time. Stage 03 will keep combining input with earlier skills before delayed recall checks begin.
