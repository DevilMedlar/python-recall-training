# Stage 03: Keyboard Input as Text

The ten normal Stage 03 drills are complete.

## Recall status

**Normal drill set: Complete on 2026-08-09.**

**Recall Check 01: Passed on 2026-08-10.**

**Recall Check 02: Active on 2026-08-11.**

This is the final delayed memory check for Stage 03. Do it from memory. Do not review earlier Stage 03 solutions, commits, or examples before attempting it.

## Recall Check 02

Create one fixed tag, collect a line and an initial mode from prompted keyboard input, reuse the stored values in a required order, then replace the mode with a later prompted keyboard value.

The first `input()` call must display exactly this prompt:

```text
Memory line: 
```

When it waits, type exactly:

```text
She said, "Input survived."
```

The second `input()` call must display exactly this prompt:

```text
Current mode: 
```

When it waits, type exactly:

```text
Waiting.
```

After those two inputs, the program must print exactly:

```text
She said, "Input survived."
[FINAL INPUT RECALL]
Waiting.

[FINAL INPUT RECALL]
She said, "Input survived."
```

Only after the first mode has already been printed, the third `input()` call must display exactly this prompt:

```text
Next mode: 
```

When it waits, type exactly:

```text
Ready!
```

After that input, the program must print exactly:

```text
Ready!
She said, "Input survived."
[FINAL INPUT RECALL]
```

### Requirements

- Create exactly three variables named `tag`, `line`, and `mode`.
- Assign the exact string `[FINAL INPUT RECALL]` to `tag` exactly once.
- Use `input()` exactly three times.
- The first `input()` call must contain the exact prompt string `Memory line: ` and store the returned keyboard text in `line`.
- The second `input()` call must contain the exact prompt string `Current mode: ` and store the returned keyboard text in `mode`.
- Print `line`, then `tag`, then `mode`.
- The fourth `print()` call must create the blank output line.
- Then print `tag` and `line` in that order.
- Only after the first `mode` value has been printed, use the third `input()` call with the exact prompt string `Next mode: ` and reassign its returned keyboard text to the same `mode` variable.
- Then print `mode`, `line`, and `tag` in that order.
- Use exactly nine `print()` calls total.
- Every non-blank `print()` call must print a variable, not a string literal directly.
- Do not reassign `tag` or `line`.
- Do not create any additional variables.
- Do not write `She said, "Input survived."`, `Waiting.`, or `Ready!` as string literals anywhere in your code.
- Use only skills already learned in Stages 01, 02, and 03.
- Type it from memory.

### Submission

Write your attempt in [`work.py`](work.py), run it locally, commit it even if it is broken, then ask for review.

Passing Recall Check 02 completes Stage 03 mastery and unlocks the next major Python feature.
