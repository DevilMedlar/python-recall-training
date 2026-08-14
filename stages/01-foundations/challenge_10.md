# Challenge 10 — Integer addition mixed with reassignment

No new Python syntax is introduced here.

This challenge mixes the integer conversion and addition from Challenge 09 with the reassignment and execution-order skill you used earlier.

Remember:

- `input()` returns text.
- `int()` converts suitable text to an integer.
- `+` adds integers.
- Reassigning a variable changes its value from that point forward.
- Output already printed before a reassignment does not change retroactively.

## Your task

Create this learner file yourself:

`stages/01-foundations/challenge_10.py`

Ask the user for two whole numbers using these exact prompts:

```text
Base number: 
Extra number: 
```

Convert both stored inputs to integers.

Create a total from the two converted integers and print that total once. Then reassign that same total variable by adding the converted base number to its current value, and print the updated total once.

Example behavior: if the user enters `4` for the base number and `3` for the extra number, the program must print:

```text
7
11
```

### Requirements

1. Use exactly five variables total.
2. Use exactly two `input()` calls.
3. The first prompt must be exactly `Base number: ` including the trailing space.
4. The second prompt must be exactly `Extra number: ` including the trailing space.
5. Store each `input()` result in its own variable before conversion.
6. Use exactly two `int()` calls.
7. Convert each stored input with `int()` and store each converted integer in a different variable.
8. Use the fifth variable as the total variable.
9. First assign that total variable the sum of the two converted integer variables.
10. Print the total variable exactly once before reassigning it.
11. Reassign only the total variable exactly once.
12. The reassignment must add the converted base-number variable to the current total using `+`.
13. Print the total variable exactly once after the reassignment.
14. Use exactly two `+` operations in the entire program.
15. Use exactly two `print()` calls, both printing the total variable.
16. Use exactly two string literals total: the two required prompts.
17. Do not reassign any variable except the total variable.
18. Do not use a blank-line `print()` in this challenge.
19. Do not use concatenation, f-strings, arithmetic other than the two required `+` operations, or any other untaught feature.
20. Do not add extra output.
21. Type the program yourself rather than copying a completed passing solution.
22. Commit the learner file when finished and say `done`.
