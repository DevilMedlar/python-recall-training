# Stage 04: Converting Text to Whole Numbers

The ten normal Stage 04 drills are complete. Recall Check 01 has passed. Arithmetic is still locked until this final delayed recall check is passed.

## Recall Check 02: Final delayed conversion recall

No copying from earlier commits. This is the last memory check for Stage 04, so keep it controlled and make every conversion land. 😏🐍

Create a fixed tag containing exactly:

```text
[FINAL INTEGER RECALL]
```

The first `input()` call must display exactly:

```text
Anchor number: 
```

When it waits, type exactly:

```text
38
```

Convert that keyboard text and preserve the integer separately.

The second `input()` call must display exactly:

```text
Current number: 
```

When it waits, type exactly:

```text
67
```

Reuse the same text variable, convert the new text, and store that integer in a number variable.

Before taking the third input, print exactly:

```text
67
38
[FINAL INTEGER RECALL]
```

Then the third `input()` call must display exactly:

```text
Next number: 
```

When it waits, type exactly:

```text
24
```

Reuse the same text variable again. Convert the newest text and reassign the same number variable that held the second converted integer.

After that third conversion, continue printing so the complete printed output is exactly:

```text
67
38
[FINAL INTEGER RECALL]
[FINAL INTEGER RECALL]
24

38
[FINAL INTEGER RECALL]
```

### Requirements

- Create exactly four variables named `tag`, `text`, `first_number`, and `number`.
- Assign the exact string `[FINAL INTEGER RECALL]` to `tag` exactly once.
- Do not reassign `tag`.
- Use `input()` exactly three times.
- The first `input()` call must contain the exact prompt string `Anchor number: ` and store its returned text in `text`.
- Convert that `text` with `int()` and store the integer in `first_number`.
- The second `input()` call must contain the exact prompt string `Current number: ` and reassign its returned text to `text`.
- Convert the new `text` with `int()` and store the integer in `number`.
- Before the third `input()` call, use exactly three `print()` calls: print `number`, then `first_number`, then `tag`.
- Only after those three prints, use the third `input()` call with the exact prompt string `Next number: ` and reassign its returned text to `text`.
- Convert the newest `text` with `int()` and reassign the integer to the same `number` variable.
- After the third conversion, print `tag`, then `number`.
- The sixth `print()` call must create the blank output line.
- Then print `first_number`, then `tag`.
- Use `int()` exactly three times total.
- Use exactly eight `print()` calls total.
- Every non-blank `print()` call must print a variable.
- Do not print `text`.
- Do not write `38`, `67`, or `24` as numeric literals or string literals anywhere in your code.
- Do not create any additional variables.
- Do not use arithmetic yet.
- Use only variables, string literals, assignment with `=`, `input()`, `int()`, and `print()`.
- Type the code yourself from memory. Do not copy from earlier Stage 04 attempts.

### Submission

Write your attempt in [`work.py`](work.py), run it locally, commit it even if it is broken, then ask for review.

If this passes, Stage 04 is mastered and the next stage can finally unlock arithmetic.
