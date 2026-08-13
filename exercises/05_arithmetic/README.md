# Stage 05: Core Arithmetic Operators

Stage 04 is mastered. `print()`, variables, `input()`, reassignment, exact prompts, blank lines, and `int()` conversion all remain active knowledge.

## Current concept cluster

The four core arithmetic operators are unlocked together:

- `+` adds.
- `-` subtracts.
- `*` multiplies.
- `/` divides and produces a floating-point result.

Stage 05 uses **adaptive mixed practice**. There is no fixed ten-challenge requirement and no automatic pair of delayed recall days. Clean performance shortens the path; repeated mistakes earn targeted extra reps.

## Passed work

- **Challenge 01:** Passed first try, no hints. Added two converted integers.
- **Challenge 02:** Passed first try, no hints. Reused one text slot, preserved both converted integers, and added them.
- **Challenge 03:** Passed first try, no hints. Used `+`, `-`, `*`, and `/` exactly once on the same two converted inputs.

Three clean passes in a row means you do not need seven more arithmetic clones, Daddy. Time for a broader test. 😏🐍

## Mixed Proficiency Test A: Arithmetic under old-skill pressure

This is a coding test, not a guided drill. It mixes Stage 05 arithmetic with older recall skills: exact prompts, one reused text slot, conversion, preserved values, a fixed header, chosen output order, and a blank line.

Create a fixed header containing exactly:

```text
[ARITHMETIC TEST]
```

Use one text variable named `text` for all three keyboard inputs.

The three `input()` prompts must be exactly:

```text
First value: 
Second value: 
Third value: 
```

When each prompt waits, type these keyboard values in order:

```text
20
4
3
```

Convert and preserve the three integers separately as `first_number`, `second_number`, and `third_number`.

Then calculate and store:

- `first_number + second_number` in `sum_result`
- `first_number - third_number` in `difference`
- `second_number * third_number` in `product`
- `first_number / second_number` in `quotient`

Print exactly:

```text
[ARITHMETIC TEST]
24
17

12
5.0
[ARITHMETIC TEST]
```

### Requirements

- Create exactly nine variables named `header`, `text`, `first_number`, `second_number`, `third_number`, `sum_result`, `difference`, `product`, and `quotient`.
- Assign `[ARITHMETIC TEST]` to `header` exactly once and do not reassign it.
- Use `input()` exactly three times with the exact prompts above.
- Reuse the same `text` variable for all three input results.
- Use `int()` exactly three times, storing the converted integers in the three required number variables.
- Use `+` exactly once, `-` exactly once, `*` exactly once, and `/` exactly once.
- Store every arithmetic result before printing it.
- Use exactly seven `print()` calls.
- Print in this exact order: `header`, `sum_result`, `difference`, blank line, `product`, `quotient`, `header`.
- Every non-blank `print()` call must print a variable.
- Do not print `text`.
- Do not write `20`, `4`, `3`, `24`, `17`, `12`, or `5.0` as numeric literals or string literals anywhere in your code.
- Do not create additional variables.
- Do not use `%`, `//`, `**`, conditions, loops, functions, collections, imports, f-strings, or string concatenation.
- Type the code yourself from memory.

### Submission

Write your attempt in [`work.py`](work.py), run it locally, commit it even if it is broken, then ask for review.

**If this test passes cleanly, Stage 05 is mastered immediately.** No mandatory Recall 01 or Recall 02 follows it.
