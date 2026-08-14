# Challenge 12 — Integer multiplication

## Tiny lesson first

You already know that integer values can be stored in variables and that `int()` converts suitable input text into an integer.

Integers can be multiplied with `*`:

```python
boxes = 4
items_per_box = 3
total = boxes * items_per_box
print(total)
```

That prints:

```text
12
```

Important distinctions:

- `*` multiplies the value on the left by the value on the right.
- Multiplying two integers produces an integer.
- Integer literals such as `6` are written without quotation marks.
- A variable can store the multiplication result.
- No new feature besides integer multiplication with `*` is introduced here.

## Your task

Create this learner file yourself:

`stages/01-foundations/challenge_12.py`

Ask the user how many packs they have. Convert that answer to an integer. Store the integer value `6` in a separate variable to represent six items per pack. Multiply the number of packs by the items-per-pack value, store the result, and print it.

Use this exact prompt:

```text
Number of packs: 
```

Example behavior: if the user enters `4`, the program must print:

```text
24
```

### Requirements

1. Use exactly four variables total.
2. Use exactly one `input()` call.
3. The prompt must be exactly `Number of packs: ` including the trailing space.
4. Store the `input()` result in its own variable before conversion.
5. Use exactly one `int()` call.
6. Convert the stored input with `int()` and store the converted integer in a different variable.
7. Store the integer literal `6` in a third variable.
8. Use the fourth variable to store the multiplication result.
9. Multiply the converted packs variable by the variable containing `6` with `*` exactly once.
10. Use exactly one integer literal in the entire program: `6`.
11. Use exactly one `print()` call.
12. The `print()` call must print the variable containing the multiplication result.
13. Use exactly one string literal in the entire program: the required prompt.
14. Do not reassign any variable.
15. Do not use `+`, `-`, division, concatenation, f-strings, or any other untaught feature.
16. Do not add extra output.
17. Type the program yourself rather than copying a completed passing solution.
18. Commit the learner file when finished and say `done`.
