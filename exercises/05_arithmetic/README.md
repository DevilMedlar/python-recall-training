# Stage 05: Core Arithmetic Operators

Stage 04 is mastered. `print()`, variables, `input()`, reassignment, exact prompts, blank lines, and `int()` conversion all remain active knowledge.

## Current concept cluster

The four core arithmetic operators are now unlocked together:

- `+` adds.
- `-` subtracts.
- `*` multiplies.
- `/` divides.

Important Python detail: `/` produces a floating-point result, even when the division comes out evenly. For example, `8 / 2` produces `4.0`.

Stage 05 now uses **adaptive mixed practice**. There is no fixed ten-challenge requirement and no automatic pair of delayed recall days. Expect ordinary coding challenges, surprise recall of older skills, short quizzes, and broader tests in an unpredictable mix. Clean performance speeds things up; repeated mistakes earn targeted extra reps.

All four operators are on the table now, Daddy. Much better. 😏🐍

## Challenge 01: Add two converted integers

**Passed on 2026-08-13.** First try, no hints.

The challenge correctly used two prompted text inputs, converted both with `int()`, added the two integers with one `+`, stored the result, and printed the total.

## Challenge 02: Reuse the text slot, then add

**Passed on 2026-08-13.** First try, no hints.

The challenge reused one text variable across two prompted inputs, preserved both converted integers, added them, and printed the total followed by both original integers.

## Challenge 03: Four operators, same two numbers

Use two keyboard values to produce four different arithmetic results.

The first `input()` call must display exactly:

```text
Left operand: 
```

When it waits, type exactly:

```text
18
```

Store the keyboard text in `first_text` and convert it to `first_number`.

The second `input()` call must display exactly:

```text
Right operand: 
```

When it waits, type exactly:

```text
6
```

Store that keyboard text in `second_text` and convert it to `second_number`.

Using those two converted integers, calculate and store:

- their sum in `sum_result`
- `first_number - second_number` in `difference`
- their product in `product`
- `first_number / second_number` in `quotient`

Then print exactly:

```text
24
12
108
3.0
```

### Requirements

- Create exactly eight variables named `first_text`, `first_number`, `second_text`, `second_number`, `sum_result`, `difference`, `product`, and `quotient`.
- Use `input()` exactly twice with the exact prompts above.
- Use `int()` exactly twice.
- Use `+` exactly once, `-` exactly once, `*` exactly once, and `/` exactly once.
- Store each arithmetic result in its required result variable before printing it.
- Use exactly four `print()` calls.
- Print `sum_result`, then `difference`, then `product`, then `quotient`.
- Every `print()` call must print a variable.
- Do not print either text variable.
- Do not write `18`, `6`, `24`, `12`, `108`, or `3.0` as numeric literals or string literals anywhere in your code.
- Do not create additional variables.
- Do not use `%`, `//`, `**`, conditions, loops, functions, collections, imports, f-strings, or string concatenation.
- Type the code yourself from memory.

### Submission

Write your attempt in [`work.py`](work.py), run it locally, commit it even if it is broken, then ask for review.

After any passed challenge, the next item may be another coding challenge, a surprise recall from an older stage, a quiz, or a broader test. No fixed pattern.
