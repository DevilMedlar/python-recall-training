# Challenge 07 — `input()` and storing user text

## Tiny lesson first

`input()` pauses the program and waits for the user to type something.

You can give `input()` a prompt string:

```python
answer = input("Type something: ")
```

When Python reaches that statement:

1. It displays the prompt `Type something: `.
2. It waits for the user to type text and press Enter.
3. `input()` returns the text the user typed.
4. The assignment stores that returned text in `answer`.

You can then print the stored value:

```python
print(answer)
```

Important distinctions:

- `input()` returns **text** in this lesson.
- The prompt string belongs inside `input()`.
- The variable stores what the user typed, not the prompt itself.
- Printing the variable later retrieves the stored user text.
- No conversion, arithmetic, concatenation, or f-strings are required or taught yet.

For this challenge, `input()` and storing its returned text are the only new Python ideas.

## Your task

Create this learner file yourself:

`stages/01-foundations/challenge_07.py`

Write a program that asks the user for one word and then prints that stored word twice.

### Required behavior

The program must first display this exact prompt:

```text
Type one word: 
```

If the user types:

```text
memory
```

then after the user presses Enter, the program must print:

```text
memory
memory
```

### Requirements

1. Create exactly one variable.
2. Use exactly one `input()` call.
3. The `input()` prompt must be exactly `Type one word: `, including the final space after the colon.
4. Store the value returned by `input()` in the variable.
5. Use exactly two `print()` calls.
6. Both `print()` calls must print the variable containing the user's input.
7. Do not reassign the variable.
8. Use exactly one string literal in the entire program: the required `input()` prompt.
9. Do not add extra output.
10. Do not use string concatenation, f-strings, conversion functions, or any other untaught feature.
11. Type the program yourself rather than copying a completed passing solution.
12. Commit the learner file to the repository when finished.

When the committed attempt is ready for grading, say `done`.
