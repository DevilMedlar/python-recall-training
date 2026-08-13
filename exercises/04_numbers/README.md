# Stage 04: Converting Text to Whole Numbers

The ten normal Stage 04 drills are complete. Arithmetic is still locked.

Today is the first delayed recall check. No copying from earlier passing commits. You have to make `input()`, `int()`, variables, reassignment, reuse, exact prompts, and exact output behave from memory.

A little pressure looks good on you. 😏

## Recall Check 01: Delayed conversion recall

Create a fixed banner containing exactly:

```text
[INTEGER RECALL]
```

The first `input()` call must display exactly:

```text
First recall: 
```

When it waits, type exactly:

```text
45
```

Convert that keyboard text and preserve the integer separately.

The second `input()` call must display exactly:

```text
Current recall: 
```

When it waits, type exactly:

```text
81
```

Reuse the same text variable, convert the new text, and store that integer in a number variable.

Before taking the third input, print exactly:

```text
45
[INTEGER RECALL]
81

[INTEGER RECALL]
```

Then the third `input()` call must display exactly:

```text
Next recall: 
```

When it waits, type exactly:

```text
26
```

Reuse the same text variable again. Convert the newest text and reassign the same number variable that held the second converted integer.

After that third conversion, continue printing so the complete printed output is exactly:

```text
45
[INTEGER RECALL]
81

[INTEGER RECALL]
26
45
[INTEGER RECALL]
```

### Requirements

- Create exactly four variables named `banner`, `text`, `first_number`, and `number`.
- Assign the exact string `[INTEGER RECALL]` to `banner` exactly once.
- Do not reassign `banner`.
- Use `input()` exactly three times.
- The first `input()` call must contain the exact prompt string `First recall: ` and store its returned text in `text`.
- Convert that `text` with `int()` and store the integer in `first_number`.
- The second `input()` call must contain the exact prompt string `Current recall: ` and reassign its returned text to `text`.
- Convert the new `text` with `int()` and store the integer in `number`.
- Before the third `input()` call, use exactly five `print()` calls: print `first_number`, then `banner`, then `number`, then create a blank output line, then print `banner` again.
- Only after those five prints, use the third `input()` call with the exact prompt string `Next recall: ` and reassign its returned text to `text`.
- Convert the newest `text` with `int()` and reassign the integer to the same `number` variable.
- After the third conversion, print `number`, then `first_number`, then `banner`.
- Use `int()` exactly three times total.
- Use exactly eight `print()` calls total.
- Every non-blank `print()` call must print a variable.
- Do not print `text`.
- Do not write `45`, `81`, or `26` as numeric literals or string literals anywhere in your code.
- Do not create any additional variables.
- Do not use arithmetic yet.
- Use only variables, string literals, assignment with `=`, `input()`, `int()`, and `print()`.
- Type the code yourself from memory. Do not copy from earlier Stage 04 attempts.

### Submission

Write your attempt in [`work.py`](work.py), run it locally, commit it even if it is broken, then ask for review.

One recall check at a time. If this passes, Recall Check 02 will still wait for another later calendar day before Stage 04 can be mastered.
