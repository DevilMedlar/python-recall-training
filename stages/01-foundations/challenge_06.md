# Challenge 06 — Reassignment and execution order

## Tiny lesson first

A variable can be assigned a new value later in the program. This is called **reassignment**.

Example:

```python
status = "First"
print(status)
status = "Second"
print(status)
```

That produces:

```text
First
Second
```

Python runs these statements from top to bottom. The first `print()` happens before the reassignment, so it sees the first value. The second `print()` happens after the reassignment, so it sees the new value.

Important distinctions:

- Reassignment uses the same variable name again on the left side of `=`.
- Reassignment changes what that name refers to from that point forward.
- Earlier output does not retroactively change.
- This challenge does not require any new feature besides reassignment.

## Your task

Create this learner file yourself:

`stages/01-foundations/challenge_06.py`

From memory, write a Python program that produces exactly this output:

```text
I remember the first value.
I remember the new value.
```

### Requirements

1. Create exactly one variable.
2. First assign the string `I remember the first value.` to that variable.
3. Print the variable exactly once before reassigning it.
4. Reassign the same variable to the string `I remember the new value.`.
5. Print the variable exactly once after the reassignment.
6. Use exactly two string literals in the entire program.
7. Use exactly two `print()` calls.
8. Both `print()` calls must print the variable, not string literals directly.
9. Match capitalization, spaces, punctuation, and order exactly.
10. Do not use `input()`.
11. Do not add extra output.
12. Type the program yourself rather than copying a completed passing solution.
13. Commit the learner file to the repository when finished.

When the committed attempt is ready for grading, say `done`.
