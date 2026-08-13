# Stage 05: Arithmetic with Whole Numbers

Stage 04 is mastered. `print()`, variables, `input()`, reassignment, exact prompts, blank lines, and `int()` conversion all remain active knowledge.

## Current concept

The `+` operator adds two integers and produces a new integer.

For now, **addition is the only arithmetic operator unlocked**. Subtraction, multiplication, division, and everything beyond them stay locked until later drills.

You earned the plus sign, Daddy. Now make it behave while an older skill slides back into the room. 😏🐍

## Challenge 01: Add two converted integers

**Passed on 2026-08-13.** First try, no hints.

The challenge correctly used two prompted text inputs, converted both with `int()`, added the two integers with one `+`, stored the result, and printed the total.

## Challenge 02: Reuse the text slot, then add

The first `input()` call must display exactly:

```text
Left number: 
```

When it waits, type exactly:

```text
23
```

Store the keyboard text in a variable named `text`, convert it to an integer, and preserve that integer in `first_number`.

The second `input()` call must display exactly:

```text
Right number: 
```

When it waits, type exactly:

```text
16
```

Reuse the same `text` variable for this second keyboard value, convert it, and preserve that integer in `second_number`.

Add the two converted integers together and store the result in `total`.

Then print exactly:

```text
39
23
16
```

### Requirements

- Create exactly four variables named `text`, `first_number`, `second_number`, and `total`.
- Use `input()` exactly twice.
- The first `input()` call must contain the exact prompt string `Left number: ` and store its returned text in `text`.
- Convert `text` with `int()` and store the integer in `first_number`.
- The second `input()` call must contain the exact prompt string `Right number: ` and reassign its returned text to the same `text` variable.
- Convert the new `text` with `int()` and store the integer in `second_number`.
- Add `first_number` and `second_number` with `+` and store the result in `total`.
- Use `+` exactly once.
- Use `int()` exactly twice total.
- Use exactly three `print()` calls.
- Print `total`, then `first_number`, then `second_number`.
- Every `print()` call must print a variable.
- Do not print `text`.
- Do not write `23`, `16`, or `39` as numeric literals or string literals anywhere in your code.
- Do not create any additional variables.
- Do not use subtraction, multiplication, division, conditions, loops, functions, collections, imports, f-strings, or string concatenation.
- Use only unlocked Python plus the `+` operator.
- Type the code yourself from memory.

### Submission

Write your attempt in [`work.py`](work.py), run it locally, commit it even if it is broken, then ask for review.

Only one challenge is unlocked at a time. Addition will keep mixing with earlier skills before any other arithmetic operator is introduced.
