# Challenge 18 — `while` loops

## Tiny lesson first

An `if` statement checks a condition once. A `while` loop keeps checking its condition and repeats its indented block while that condition remains `True`.

```python
count = 3
while count > 0:
    print(count)
    count = count - 1
print("done")
```

That produces:

```text
3
2
1
done
```

The important mental model is:

1. Python checks the `while` condition.
2. If it is `True`, the indented body runs.
3. Execution returns to the `while` condition and checks again.
4. When the condition becomes `False`, Python leaves the loop and continues with the next unindented statement.

A loop must usually change something involved in its condition. Otherwise the condition may never become false and the loop can continue indefinitely.

For this challenge, `while` is the only new Python syntax. Reassignment, subtraction, comparisons, input, conversion, and `print()` are all previously unlocked.

## Your task

Create this learner file yourself:

`stages/01-foundations/challenge_18.py`

Ask the user for a starting count, convert it to an integer, then count downward to `1` using a `while` loop. After the loop finishes, print `done`.

Use this prompt:

```text
Start count: 
```

Example behavior: if the user enters `3`, the program must output:

```text
3
2
1
done
```

### Requirements

1. Use exactly two variables total.
2. Use exactly one `input()` call.
3. Use the prompt `Start count: ` including the trailing space.
4. Store the raw input in one variable before conversion.
5. Use exactly one `int()` call and store the converted integer in the second variable.
6. Use exactly one `while` loop.
7. The `while` condition must compare the converted integer variable to `0` using `>` exactly once.
8. End the `while` line with a colon.
9. Inside the loop, first print the converted integer variable.
10. Inside the loop, after that print, reassign the same integer variable by subtracting `1` from its current value.
11. Use `-` exactly once in the source code.
12. The loop body must contain exactly those two statements, both indented.
13. After the loop, use one unindented `print()` call to print `done`.
14. Use exactly two `print()` calls in the source code total: one inside the loop and one after it.
15. Use exactly two string literals total: the prompt and `done`.
16. Use exactly two integer literal values total: `0` and `1`.
17. Do not use `if`, `elif`, `else`, `<`, `==`, `+`, `*`, `/`, boolean literals, nested loops, or any other untaught feature.
18. Do not add extra output.
19. Type the program yourself rather than copying a completed passing solution.
20. Commit the learner file when finished and say `done`.
