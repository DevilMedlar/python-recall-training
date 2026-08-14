# Stage 01 — Foundations Grade Ledger

Tutor-owned progress metadata for the current fresh-start run. Record challenge grades, grading attempts, hints, notable strengths/weaknesses, and reward/correction continuity here without altering learner answer files.

| Challenge | Grade | Grading attempts | Hints used | Status | Notes |
|---|---:|---:|---:|---|---|
| 01 | 100% | 1 | 0 | PASS | Clean first graded attempt. Exact string output with three `print()` calls. Static/visual grading only. Full 100% reward, no correction. |
| 02 | 100% final | 2 | 1 | PASS | First graded attempt was approximately 88%: visible output was correct, but the required blank-line construction used `print("")` instead of the explicitly required empty `print()`. Hint 1 identified the requirement-form mistake without giving the correction. Second committed attempt repaired it and passed 100%. Static/visual grading only. |
| 03 | 100% | 1 | 0 | PASS | Clean first graded attempt. Correctly recalled two empty `print()` calls in a different arrangement, showing the Challenge 02 exact-construction weakness did not immediately repeat. Static/visual grading only. Full 100% reward, no correction. |
| 04 | 100% | 1 | 0 | PASS | First clean use of one variable, assignment, and reuse. Exactly one string literal and two `print()` calls using the variable. Static/visual grading only. Full 100% reward, no correction. |
| 05 | 100% | 1 | 0 | PASS | Clean mixed recall of two variables, reuse, and one empty `print()` blank line. Exactly two literals and five `print()` calls. Static/visual grading only. Full 100% reward, no correction. |
| 06 | 100% | 1 | 0 | PASS | Clean first reassignment challenge. Same variable printed before and after reassignment with correct execution order. Static/visual grading only. Full 100% reward, no correction. |
| 07 | 100% | 1 | 0 | PASS | First graded attempt was clean. Exactly one variable, one exact `input()` prompt, two `print()` calls, one string literal, no reassignment, and the stored user text is reused correctly. Static/visual grading only; code was fetched and inspected, not executed. Full 100% reward, no correction. |
| 08 | 100% | 1 | 0 | PASS | Clean first graded attempt. Exactly two variables, two exact `input()` prompts, two string literals, three `print()` calls with one empty call, and the two stored inputs are printed in reverse order without reassignment. Static/visual grading only; code was fetched and inspected, not executed. Full 100% reward, no correction. |
| 09 | 100% | 1 | 0 | PASS | Clean first graded attempt on numeric conversion and addition. Exactly five variables, two exact `input()` prompts, two stored raw text values, two `int()` conversions stored separately, one `+` operation stored in the fifth variable, then an empty `print()` and a print of the sum. Static/visual grading only; code was fetched and inspected, not executed. Full 100% reward, no correction. |
| 10 | 100% | 1 | 0 | PASS | Clean mixed recall of integer conversion, addition, reassignment, and execution order. Exactly five variables, two exact prompts, two stored raw inputs, two `int()` conversions, two `+` operations, and two prints of the same total variable before and after its single reassignment. Static/visual grading only; code was fetched and inspected, not executed. Full 100% reward, no correction. |
| 11 | 100% | 1 | 0 | PASS | Clean first graded use of integer subtraction. Exactly five variables, two exact prompts, two stored raw inputs, two `int()` conversions, one correctly ordered `-` operation stored in the fifth variable, and one print of the result. Static/visual grading only; code was fetched and inspected, not executed. Full 100% reward, no correction. |
| 12 | 100% | 1 | 0 | PASS | Clean first graded use of integer multiplication. Exactly four variables, one exact `input()` prompt, one stored raw input, one `int()` conversion, the single integer literal `6` stored separately, one `*` operation stored in the fourth variable, and one print of the result. Static/visual grading only; code was fetched and inspected, not executed. Full 100% reward, no correction. |
| 13 | 100% | 1 | 0 | PASS | Clean first graded use of normal division. Exactly five variables, two exact prompts, two stored raw inputs, two `int()` conversions, one correctly ordered `/` operation stored in the fifth variable, and one print of the unconverted division result. Static/visual grading only; code was fetched and inspected, not executed. Full 100% reward, no correction. |
| 14 | ~95% | 1 | 1 | RETRY | Mixed arithmetic structure is otherwise clean: five variables, two inputs, two `int()` conversions, one result variable, correct `+`, `-`, `*`, `/` sequence, four prints, and preserved float division result. One exact-prompt formatting requirement is wrong in the first `input()` call, so the challenge is not yet passed. Hint 1 identified only the category/location of that mismatch. Static/visual grading only; code was fetched and inspected, not executed. |

## Current evidence notes

- Exact output, capitalization, punctuation, and ordering have been consistently clean across the current run, with a new exact-prompt formatting miss observed on Challenge 14.
- One earlier observed weakness: exact blank-line construction on Challenge 02 (`print("")` versus explicitly required empty `print()`). It was repaired after one Hint 1 and then recalled correctly on later challenges.
- Variable assignment and reuse: clean on Challenges 04 and 05.
- Reassignment timing and top-to-bottom execution order: clean on Challenges 06, 10, and structurally clean on Challenge 14 first attempt.
- `input()` prompt placement and exact trailing-space precision: clean on Challenges 07–13; Challenge 14 first attempt introduced one exact-prompt formatting miss in the first `input()` call.
- Storing and reusing values returned by `input()`: clean on Challenges 07 and 08.
- Two-input variable separation and reverse-order retrieval: clean on Challenge 08.
- Distinguishing raw `input()` text from converted integers: clean on Challenges 09–14.
- `int()` conversion and integer addition with `+`: clean across Challenges 09, 10, and structurally correct in Challenge 14 first attempt.
- Integer subtraction with `-`, including operand order: clean on Challenge 11 and structurally correct in Challenge 14 first attempt.
- Integer multiplication with `*`: clean on Challenge 12 and structurally correct in Challenge 14 first attempt.
- Normal division with `/`, including operand order and preserving the float result: clean on Challenge 13 and structurally correct in Challenge 14 first attempt.
- Current fresh-run meaningful hint total through Challenge 14 first attempt: 2.
