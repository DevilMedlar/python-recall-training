# Stage 04: Converting Text to Whole Numbers

Stage 03 is mastered. Keyboard input, variables, reuse, reassignment, exact output, and prompt text remain active knowledge and will keep returning.

## Current concept

`input()` always returns text, even when the user types digits.

`int()` converts valid whole-number text into an integer. Separate keyboard inputs can be converted separately, stored in different variables, and printed in any order.

Arithmetic is still locked. For now, the job is to recognize when a value is still text and when it has been converted into an integer.

## Challenge 02: Two conversions, reverse output

Run the program. The first `input()` call must display exactly:

```text
First number: 
```

When it waits, type exactly:

```text
17
```

The second `input()` call must display exactly:

```text
Second number: 
```

When it waits, type exactly:

```text
29
```

After both values have been entered and converted, the program must print exactly:

```text
29
17
```

### Requirements

- Create exactly four variables named `first_text`, `first_number`, `second_text`, and `second_number`.
- Use `input()` exactly twice.
- The first `input()` call must contain the exact prompt string `First number: ` and store the returned text in `first_text`.
- Use `int()` to convert `first_text` and store the integer in `first_number`.
- The second `input()` call must contain the exact prompt string `Second number: ` and store the returned text in `second_text`.
- Use `int()` to convert `second_text` and store the integer in `second_number`.
- Use `int()` exactly twice total.
- Use exactly two `print()` calls.
- First print `second_number`.
- Then print `first_number`.
- Do not print either text variable.
- Do not write `17` or `29` as numeric literals or string literals anywhere in your code.
- Do not create any additional variables.
- Do not use arithmetic yet.
- Use only variables, string literals, assignment with `=`, `input()`, `int()`, and `print()`.
- Type the code yourself.

### Submission

Write your attempt in [`work.py`](work.py), run it locally, commit it even if it is broken, then ask for review.

Only one challenge is unlocked at a time. Number conversion will keep repeating and mixing with earlier skills before arithmetic is introduced.
