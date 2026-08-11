# Stage 04: Converting Text to Whole Numbers

Stage 03 is mastered. Keyboard input, variables, reuse, reassignment, exact output, prompt text, and blank lines remain active knowledge and will keep returning.

## Current concept

`input()` returns text, and `int()` converts valid whole-number text into an integer.

Challenge 06 combines two separate conversions with a fixed tag, chosen output order, reuse, and a blank line. Arithmetic is still locked.

## Challenge 06: Two converted values with a fixed tag

Create a fixed tag containing exactly:

```text
[INTEGER LOG]
```

The first `input()` call must display exactly:

```text
First value: 
```

When it waits, type exactly:

```text
14
```

Convert that keyboard text into an integer.

The second `input()` call must display exactly:

```text
Second value: 
```

When it waits, type exactly:

```text
73
```

Convert that keyboard text into an integer.

After both values have been entered and converted, use your stored variables to print exactly:

```text
[INTEGER LOG]
73
14

73
[INTEGER LOG]
```

### Requirements

- Create exactly five variables named `tag`, `first_text`, `first_number`, `second_text`, and `second_number`.
- Assign the exact string `[INTEGER LOG]` to `tag` exactly once.
- Do not reassign `tag`.
- Use `input()` exactly twice.
- The first `input()` call must contain the exact prompt string `First value: ` and store its returned text in `first_text`.
- Use `int()` to convert `first_text` and store the integer in `first_number`.
- The second `input()` call must contain the exact prompt string `Second value: ` and store its returned text in `second_text`.
- Use `int()` to convert `second_text` and store the integer in `second_number`.
- Use `int()` exactly twice total.
- Use exactly six `print()` calls.
- Print `tag`, then `second_number`, then `first_number`.
- The fourth `print()` call must create the blank output line.
- Then print `second_number`, then `tag`.
- Every non-blank `print()` call must print a variable.
- Do not print either text variable.
- Do not write `14` or `73` as numeric literals or string literals anywhere in your code.
- Do not create any additional variables.
- Do not use arithmetic yet.
- Use only variables, string literals, assignment with `=`, `input()`, `int()`, and `print()`.
- Type the code yourself.

### Submission

Write your attempt in [`work.py`](work.py), run it locally, commit it even if it is broken, then ask for review.

Only one challenge is unlocked at a time. Number conversion will keep repeating and mixing with earlier skills before arithmetic is introduced.
