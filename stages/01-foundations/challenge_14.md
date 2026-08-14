# Challenge 14 — Mixed arithmetic proficiency check

No new Python syntax is introduced here.

This challenge mixes skills you have already unlocked:

- `input()` returning text
- `int()` conversion
- variable assignment and reassignment
- integer addition with `+`
- integer subtraction with `-`
- integer multiplication with `*`
- normal division with `/`
- `/` producing a float
- execution order

## Your task

Create this learner file yourself:

`stages/01-foundations/challenge_14.py`

Ask the user for two whole numbers. Assume the second number is non-zero.

Use these exact prompts:

```text
First number: 
Second non-zero number: 
```

Store each raw input separately, convert each to an integer, then use one result variable for all four calculations in this exact sequence:

1. Add the two converted integers and print the result.
2. Reassign the same result variable to the first converted integer minus the second converted integer, then print it.
3. Reassign the same result variable to the first converted integer multiplied by the second converted integer, then print it.
4. Reassign the same result variable to the first converted integer divided by the second converted integer, then print it.

Example behavior: if the user enters `8` and then `2`, the program must print:

```text
10
6
16
4.0
```

### Requirements

1. Use exactly five variables total.
2. Use exactly two `input()` calls.
3. The first prompt must be exactly `First number: ` including the trailing space.
4. The second prompt must be exactly `Second non-zero number: ` including the trailing space.
5. Store each `input()` result in its own variable before conversion.
6. Use exactly two `int()` calls.
7. Convert each stored input with `int()` and store each converted integer in a different variable.
8. Use the fifth variable as the result variable for all four calculations.
9. First assign the result variable using `+` exactly once and print it.
10. Reassign that same result variable using `-` exactly once and print it.
11. Reassign that same result variable using `*` exactly once and print it.
12. Reassign that same result variable using `/` exactly once and print it.
13. Use exactly one `+`, one `-`, one `*`, and one `/` operation in the entire program.
14. Use exactly four `print()` calls, each printing the same result variable.
15. Use exactly two string literals total: the two required prompts.
16. Do not convert the division result to `int()` or any other type.
17. Do not reassign any variable except the result variable.
18. Do not use blank-line `print()` calls, concatenation, f-strings, or any other untaught feature.
19. Do not add extra output.
20. Type the program yourself rather than copying a completed passing solution.
21. Commit the learner file when finished and say `done`.
