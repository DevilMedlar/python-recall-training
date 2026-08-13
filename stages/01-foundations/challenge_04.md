# Challenge 04 — Variables, assignment, and reuse

## Tiny lesson first

A variable is a name that refers to a value.

You can assign a string to a variable with `=`:

```python
message = "Hello"
```

After that assignment, `message` refers to the string `"Hello"`.

You can pass the variable to `print()` instead of writing the string again:

```python
print(message)
```

That prints:

```text
Hello
```

Important distinctions:

- The name on the left side of `=` is the variable name.
- `=` performs assignment here. It gives the name a value.
- The quotation marks belong around the string value, not around the variable name when you use it.
- Reusing the same variable lets the program reuse the stored value without repeating the string literal.
- Variable names are case-sensitive.

For this challenge, assignment and printing a variable are the only new Python ideas.

## Your task

Create this learner file yourself:

`stages/01-foundations/challenge_04.py`

From memory, write a Python program that produces exactly this output:

```text
Recall makes it mine.
Recall makes it mine.
```

### Requirements

1. Create exactly one variable.
2. Assign the string `Recall makes it mine.` to that variable exactly once.
3. Use exactly one string literal in the entire program.
4. Use exactly two `print()` calls.
5. Both `print()` calls must print the variable, not repeat the string literal directly.
6. Match capitalization, spaces, punctuation, and order exactly.
7. Do not use `input()`.
8. Do not add extra output.
9. Type the program yourself rather than copying a completed passing solution.
10. Commit the learner file to the repository when finished.

When the committed attempt is ready for grading, say `done`.
