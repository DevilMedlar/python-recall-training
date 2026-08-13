# Stage 04 - `input()` and Text Input

## Goal

Learn how Python pauses to receive text from the user, then stores that text in a variable.

## Tiny lesson

`input()` is a built-in Python function that waits for the user to type something and press Enter.

You can store what the user typed in a variable:

```python
name = input("Name: ")
```

The string inside `input()` is the prompt shown to the user.

For now, remember one important fact: **`input()` returns text**. Even if the user types digits, Python gives you a string unless you explicitly convert it later.

You can then print the stored response:

```python
print(name)
```

For this challenge, use only what has already been taught: `print()`, quoted strings, variables, assignment/reassignment, and `input()`.

## Challenge 01

Write the solution yourself in `learner.py`.

### Requirements

1. Create a variable named `answer`.
2. Use exactly one `input()` call.
3. The input prompt must be exactly `Type something: ` including the final space after the colon.
4. Store the result of `input()` in `answer`.
5. Use exactly one `print()` call.
6. The `print()` call must print the variable `answer`.
7. Do not create any other variables.
8. Do not add any extra output beyond the input prompt and the echoed answer.
9. Type the Python yourself from memory.

## What should happen

If the user types:

```text
Python
```

then the interaction should look like:

```text
Type something: Python
Python
```

Commit your attempt, then tell Senpai `done`.
