# Stage 03: Keyboard Input as Text

The ten normal Stage 03 drills are complete.

## Recall status

**Normal drill set: Complete on 2026-08-09.**

**Recall Check 01: Active on 2026-08-10.**

This is a delayed memory check. Do it from memory. Do not review earlier Stage 03 solutions, commits, or examples before attempting it.

## Recall Check 01

Create a fixed banner, collect a message and an initial state from prompted keyboard input, print them in the required order, then replace the state with a later prompted keyboard value.

The first `input()` call must display exactly this prompt:

```text
Recall text: 
```

When it waits, type exactly:

```text
She said, "Still stored."
```

The second `input()` call must display exactly this prompt:

```text
First state: 
```

When it waits, type exactly:

```text
Waiting.
```

After those two inputs, the program must print exactly:

```text
[INPUT RECALL]
She said, "Still stored."
Waiting.

She said, "Still stored."
```

Only after the first state has already been printed, the third `input()` call must display exactly this prompt:

```text
Second state: 
```

When it waits, type exactly:

```text
Ready!
```

After that input, the program must print exactly:

```text
[INPUT RECALL]
Ready!
[INPUT RECALL]
```

### Requirements

- Create exactly three variables named `banner`, `message`, and `state`.
- Assign the exact string `[INPUT RECALL]` to `banner` exactly once.
- Use `input()` exactly three times.
- The first `input()` call must contain the exact prompt string `Recall text: ` and store the returned keyboard text in `message`.
- The second `input()` call must contain the exact prompt string `First state: ` and store the returned keyboard text in `state`.
- Print `banner`, then `message`, then `state`.
- The fourth `print()` call must create the blank output line.
- Print `message` again after the blank line.
- Only after the first `state` value has been printed, use the third `input()` call with the exact prompt string `Second state: ` and reassign its returned keyboard text to the same `state` variable.
- Then print `banner`, `state`, and `banner` in that order.
- Use exactly eight `print()` calls total.
- Every non-blank `print()` call must print a variable, not a string literal directly.
- Do not reassign `banner` or `message`.
- Do not create any additional variables.
- Do not write `She said, "Still stored."`, `Waiting.`, or `Ready!` as string literals anywhere in your code.
- Use only skills already learned in Stages 01, 02, and 03.
- Type it from memory.

### Submission

Write your attempt in [`work.py`](work.py), run it locally, commit it even if it is broken, then ask for review.

Passing Recall Check 01 will not master Stage 03 yet. A second delayed recall check on another later calendar day will still be required before another major Python feature unlocks.
