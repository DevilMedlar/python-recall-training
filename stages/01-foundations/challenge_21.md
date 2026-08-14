# Challenge 21 — mixed control-flow proficiency

## No new syntax

Everything in this challenge has already been taught. This is a transfer test: you must choose and combine the right unlocked tools without being shown the finished structure.

Remember the behavior you already know:

- `input()` returns text, so numeric comparison requires conversion.
- `range(start, stop)` includes the start and excludes the stop.
- `continue` skips only the current iteration.
- `break` exits the current loop completely.
- A `for` loop supplies each next value to its loop variable automatically.

## Your task

Create this learner file yourself:

`stages/01-foundations/challenge_21.py`

Ask the user for a stopping limit with this exact prompt:

```text
Stop after: 
```

Convert the response to an integer.

Then loop through the integers produced by `range(1, 9)`.

Inside the loop:

- skip the value `3`
- stop the loop as soon as the loop variable becomes greater than the converted stopping limit
- otherwise print the loop variable

After the loop finishes, print `done`.

Example behavior if the user enters `6`:

```text
1
2
4
5
6
done
```

Example behavior if the user enters `2`:

```text
1
2
done
```

### Requirements

1. Use exactly three variables total: one raw-input variable, one converted-limit variable, and one loop variable.
2. Use exactly one `input()` call with the prompt `Stop after: ` including the trailing space.
3. Store the raw input before conversion.
4. Use exactly one `int()` call and store the converted result in the second variable.
5. Use exactly one `for` loop.
6. Use exactly one `range()` call with exactly two arguments: `1` and `9`.
7. Inside the loop, use exactly two `if` statements.
8. One `if` must compare the loop variable to `3` using `==`, and its body must contain exactly one `continue`.
9. The other `if` must compare the loop variable to the converted stopping-limit variable using `>`, and its body must contain exactly one `break`.
10. Both control-flow checks must happen before the loop-body `print()`.
11. After those checks, still inside the loop, use exactly one `print()` call that prints the loop variable.
12. After the loop, use one unindented `print()` call that prints the string `done`.
13. Use exactly two `print()` calls in the source code total.
14. Do not manually reassign the loop variable.
15. Do not use `while`, `elif`, `else`, `<`, arithmetic operators, boolean literals, nested loops, or any other untaught feature.
16. Do not add extra output.
17. Type the program yourself rather than copying a completed passing solution.
18. Commit the learner file when finished and say `done`.
