# Stage 04: Converting Text to Whole Numbers

Stage 03 is mastered. Keyboard input, variables, reuse, reassignment, exact output, prompt text, and blank lines remain active knowledge and will keep returning.

## Current concept

`input()` returns text, and `int()` converts valid whole-number text into an integer.

Challenge 09 keeps one text variable moving through three prompted inputs while preserving all three converted integers separately. Arithmetic is still locked.

## Challenge 09: Three conversions, one text slot

Create a fixed header containing exactly:

```text
[INTEGER TRIO]
```

The first `input()` call must display exactly:

```text
First value: 
```

When it waits, type exactly:

```text
13
```

Convert that keyboard text and store the integer separately.

The second `input()` call must display exactly:

```text
Second value: 
```

When it waits, type exactly:

```text
47
```

Reuse the same text variable, convert the new text, and preserve that integer separately.

The third `input()` call must display exactly:

```text
Third value: 
```

When it waits, type exactly:

```text
92
```

Reuse the same text variable again, convert the new text, and preserve that integer separately.

After all three conversions, print exactly:

```text
92
13
[INTEGER TRIO]

47
92
13
[INTEGER TRIO]
```

### Requirements

- Create exactly five variables named `header`, `text`, `first_number`, `second_number`, and `third_number`.
- Assign the exact string `[INTEGER TRIO]` to `header` exactly once.
- Do not reassign `header`.
- Use `input()` exactly three times.
- The first `input()` call must contain the exact prompt string `First value: ` and store its returned text in `text`.
- Use `int()` to convert `text` and store the integer in `first_number`.
- The second `input()` call must contain the exact prompt string `Second value: ` and reassign its returned text to the same `text` variable.
- Use `int()` to convert the new `text` and store the integer in `second_number`.
- The third `input()` call must contain the exact prompt string `Third value: ` and reassign its returned text to the same `text` variable again.
- Use `int()` to convert the new `text` and store the integer in `third_number`.
- Use `int()` exactly three times total.
- Use exactly eight `print()` calls.
- Print `third_number`, then `first_number`, then `header`.
- The fourth `print()` call must create the blank output line.
- Then print `second_number`, then `third_number`, then `first_number`, then `header`.
- Every non-blank `print()` call must print a variable.
- Do not print `text`.
- Do not write `13`, `47`, or `92` as numeric literals or string literals anywhere in your code.
- Do not create any additional variables.
- Do not use arithmetic yet.
- Use only variables, string literals, assignment with `=`, `input()`, `int()`, and `print()`.
- Type the code yourself.

### Submission

Write your attempt in [`work.py`](work.py), run it locally, commit it even if it is broken, then ask for review.

Only one challenge is unlocked at a time. Number conversion will keep repeating and mixing with earlier skills before arithmetic is introduced.
