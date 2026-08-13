# Stage 06: More Arithmetic Operators

Stage 05 is mastered. All earlier skills remain active and can return without warning.

## Current concept cluster

Three more arithmetic operators are unlocked together:

- `%` gives the remainder after division.
- `//` performs floor division. With positive whole numbers, it gives the whole-number quotient with the remainder discarded.
- `**` performs exponentiation: the left value raised to the power of the right value.

Examples with unrelated values:

- `11 % 4` produces `3`.
- `11 // 4` produces `2`.
- `3 ** 2` produces `9`.

Quiz B was a clean 5/5, so we keep moving. One earlier wobble on reassignment is being folded into this challenge instead of becoming a whole remedial stage. 😏🐍

## Challenge 01: Three operators, one result slot

The first `input()` call must display exactly:

```text
Base value: 
```

When it waits, type exactly:

```text
9
```

Store the keyboard text in `text`, convert it with `int()`, and preserve the integer in `first_number`.

The second `input()` call must display exactly:

```text
Other value: 
```

When it waits, type exactly:

```text
2
```

Reuse the same `text` variable, convert it, and preserve the integer in `second_number`.

Then reuse one variable named `result` three times:

1. Store `first_number % second_number` in `result`, then print `result`.
2. Reassign `result` to `first_number // second_number`, then print `result`.
3. Reassign `result` to `first_number ** second_number`, then print `result`.

The printed output must be exactly:

```text
1
4
81
```

### Requirements

- Create exactly four variables named `text`, `first_number`, `second_number`, and `result`.
- Use `input()` exactly twice with the exact prompts above.
- Reuse the same `text` variable for both input results.
- Use `int()` exactly twice.
- Use `%` exactly once.
- Use `//` exactly once.
- Use `**` exactly once.
- Reassign the same `result` variable for all three calculations.
- Use exactly three `print()` calls, each printing `result` immediately after the corresponding calculation.
- Do not print `text`.
- Do not write `9`, `2`, `1`, `4`, or `81` as numeric literals or string literals anywhere in your code.
- Do not create additional variables.
- Do not use conditions, loops, functions, collections, imports, f-strings, or string concatenation.
- Type the code yourself from memory.

### Submission

Write your attempt in [`work.py`](work.py), run it locally, commit it even if it is broken, then ask for review.

Adaptive pacing is still active. After this, the next item may mix these operators with older arithmetic, test precedence, pull an old skill back in, or jump to a quiz/test depending on performance.
