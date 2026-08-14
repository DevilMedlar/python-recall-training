# Challenge 17 — `elif` and three-way branching

## Tiny lesson first

An `if`/`else` pair chooses between two paths. `elif` lets Python check another condition when the earlier `if` condition was false.

```python
number = 10
if number > 10:
    print("high")
elif number == 10:
    print("equal")
else:
    print("low")
```

Python checks the branches from top to bottom:

1. If the `if` condition is true, its block runs and the rest of this chain is skipped.
2. Otherwise Python checks the `elif` condition.
3. If neither condition is true, the `else` block runs.

For one connected `if` / `elif` / `else` chain, exactly one branch runs.

Important details:

- `elif` means "else if".
- `elif` has its own condition.
- `if` and `elif` condition lines end with `:`.
- `else` ends with `:` but has no condition.
- Each branch body is indented.

For this challenge, `elif` is the only new Python syntax.

## Your task

Create this learner file yourself:

`stages/01-foundations/challenge_17.py`

Ask the user for one whole number and convert it to an integer.

Use this prompt:

```text
Enter level: 
```

Then create one three-way branch:

- if the number is greater than `10`, print `high`
- elif the number equals `10`, print `equal`
- else, print `low`

The output words are deliberately punctuation-free so this challenge measures branching rather than cosmetic punctuation.

### Requirements

1. Use exactly two variables total.
2. Use exactly one `input()` call.
3. Use the prompt `Enter level: ` including the trailing space.
4. Store the raw input before conversion.
5. Use exactly one `int()` call and store the converted value in the second variable.
6. Use exactly one `if` statement.
7. The `if` condition must compare the converted integer to `10` using `>` exactly once.
8. Use exactly one `elif` paired with that `if`.
9. The `elif` condition must compare the converted integer to `10` using `==` exactly once.
10. Use exactly one final `else` paired with that chain.
11. End the `if`, `elif`, and `else` lines with colons.
12. Indent each branch body.
13. Use exactly three `print()` calls total, one in each branch.
14. The three branch outputs must be `high`, `equal`, and `low` in the matching branches.
15. Use exactly four string literals total: the prompt plus those three output words.
16. Use exactly one integer literal value in the program: `10` (it may appear in both comparisons).
17. Do not use `<`, arithmetic operators, boolean literals, nested conditions, or additional comparisons.
18. Do not add extra output.
19. Type the program yourself rather than copying a completed passing solution.
20. Commit the learner file when finished and say `done`.
