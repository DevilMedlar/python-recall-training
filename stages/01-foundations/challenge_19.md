# Challenge 19 — `for` loops and `range()`

## Tiny lesson first

A `while` loop repeats while a condition remains `True`. A `for` loop can instead take values from a sequence one at a time.

`range()` can produce a sequence of integers for a `for` loop:

```python
for number in range(2, 5):
    print(number)
```

That produces:

```text
2
3
4
```

Important mental model:

- `for` assigns the next value from the sequence to the loop variable.
- `in` connects the loop variable to the sequence being traversed.
- `range(start, stop)` includes `start` but does **not** include `stop`.
- The indented body runs once for each value produced by `range()`.
- When there are no values left, execution continues with the next unindented statement.

For this challenge, `for`, `in`, and `range()` are the new Python ideas.

## Your task

Create this learner file yourself:

`stages/01-foundations/challenge_19.py`

Use a `for` loop with `range()` to print the integers from `4` through `7`, one per line. After the loop finishes, print `done`.

The program should output:

```text
4
5
6
7
done
```

### Requirements

1. Use exactly one variable total: the loop variable.
2. Use exactly one `for` loop.
3. Use exactly one `range()` call.
4. Call `range()` with exactly two arguments.
5. The `range()` start argument must be the integer literal `4`.
6. The `range()` stop argument must be the integer literal `8`.
7. The `for` line must use `in` and end with a colon.
8. Inside the loop, use exactly one indented `print()` call that prints the loop variable.
9. After the loop, use exactly one unindented `print()` call that prints `done`.
10. Use exactly two `print()` calls in the source code total.
11. Use exactly one string literal in the entire program: `done`.
12. Use exactly two integer literal values in the entire program: `4` and `8`.
13. Do not reassign the loop variable yourself.
14. Do not use `input()`, `int()`, `while`, `if`, `elif`, `else`, arithmetic operators, comparison operators, boolean literals, nested loops, or any other untaught feature.
15. Do not add extra output.
16. Type the program yourself rather than copying a completed passing solution.
17. Commit the learner file when finished and say `done`.
