# Stage 05: Arithmetic with Whole Numbers

Stage 04 is mastered. `print()`, variables, `input()`, reassignment, exact prompts, blank lines, and `int()` conversion all remain active knowledge.

## Current concept

The `+` operator adds two integers and produces a new integer.

For now, **addition is the only arithmetic operator unlocked**. Subtraction, multiplication, division, and everything beyond them stay locked until later drills.

You finally earned the plus sign, Daddy. Don't get greedy with it yet. 😏🐍

## Challenge 01: Add two converted integers

The first `input()` call must display exactly:

```text
First addend: 
```

When it waits, type exactly:

```text
12
```

Store the keyboard text, convert it to an integer, and preserve that integer.

The second `input()` call must display exactly:

```text
Second addend: 
```

When it waits, type exactly:

```text
7
```

Store that keyboard text separately and convert it to an integer.

Add the two converted integers together, store the result, then print exactly:

```text
19
```

### Requirements

- Create exactly five variables named `first_text`, `first_number`, `second_text`, `second_number`, and `total`.
- Use `input()` exactly twice.
- The first `input()` call must contain the exact prompt string `First addend: ` and store its returned text in `first_text`.
- Convert `first_text` with `int()` and store the integer in `first_number`.
- The second `input()` call must contain the exact prompt string `Second addend: ` and store its returned text in `second_text`.
- Convert `second_text` with `int()` and store the integer in `second_number`.
- Add `first_number` and `second_number` with `+` and store the result in `total`.
- Use `+` exactly once.
- Use `int()` exactly twice total.
- Use exactly one `print()` call, and it must print `total`.
- Do not print either text variable.
- Do not write `12`, `7`, or `19` as numeric literals or string literals anywhere in your code.
- Do not create any additional variables.
- Do not use subtraction, multiplication, division, conditions, loops, functions, collections, imports, f-strings, or string concatenation.
- Use only unlocked Python plus the newly unlocked `+` operator.
- Type the code yourself from memory.

### Submission

Write your attempt in [`work.py`](work.py), run it locally, commit it even if it is broken, then ask for review.

Only one challenge is unlocked at a time. Addition will repeat and mix with earlier skills before any other arithmetic operator is introduced.
