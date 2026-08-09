# Stage 03: Keyboard Input as Text

Stage 02 is mastered. Variables, reassignment, exact output, quotation marks, and blank lines remain active knowledge and will keep returning.

## Current concept

You now know how to collect keyboard text with `input()`, add prompt text, store multiple values, reuse stored input, and reassign a variable from a later input.

Challenge 10 is the normal-drill capstone for Stage 03. It combines those skills with older variable and exact-output skills. No new syntax is introduced.

## Challenge 10: Input capstone

Create one fixed header, collect a message, then collect two different states in the same `state` variable.

The first `input()` call must display exactly this prompt:

```text
Message: 
```

When it waits, type exactly:

```text
She said, "Keyboard memory."
```

The second `input()` call must display exactly this prompt:

```text
State one: 
```

When it waits, type exactly:

```text
Waiting.
```

After those two inputs, print exactly:

```text
She said, "Keyboard memory."
[INPUT CAPSTONE]
Waiting.

```

Then the third `input()` call must display exactly this prompt:

```text
State two: 
```

When it waits, type exactly:

```text
Ready!
```

After that input, print exactly:

```text
[INPUT CAPSTONE]
Ready!
She said, "Keyboard memory."
```

### Requirements

- Create exactly three variables named `header`, `message`, and `state`.
- Assign the exact string `[INPUT CAPSTONE]` to `header` exactly once.
- Use `input()` exactly three times.
- The first `input()` call must contain the exact prompt string `Message: ` and store the returned keyboard text in `message`.
- The second `input()` call must contain the exact prompt string `State one: ` and store the returned keyboard text in `state`.
- Print `message`, then `header`, then `state`.
- The fourth `print()` call must create the blank output line.
- Only after the first `state` value has been printed, use a third `input()` call with the exact prompt string `State two: ` and reassign its returned keyboard text to the same `state` variable.
- Then print `header`, `state`, and `message` in that order.
- Use exactly seven `print()` calls total.
- Every non-blank `print()` call must print a variable, not a string literal directly.
- Do not reassign `header` or `message`.
- Do not create any additional variables.
- Do not write `She said, "Keyboard memory."`, `Waiting.`, or `Ready!` as string literals anywhere in your code.
- Use only variables, string literals, assignment with `=`, `input()`, and `print()`.
- Type the code yourself.

### Submission

Write your attempt in [`work.py`](work.py), run it locally, commit it even if it is broken, then ask for review.

Passing this challenge completes the normal Stage 03 drill set. Delayed recall checks are still required before Stage 03 is mastered and another major Python feature unlocks.
