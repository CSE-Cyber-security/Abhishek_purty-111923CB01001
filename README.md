# Password Strength Checker

A Python command-line program that checks a password against five rules and reports which ones are satisfied.

## Rules

| Criterion | Requirement |
| --- | --- |
| Length | At least 8 characters |
| Uppercase | At least one ASCII uppercase letter (`A`–`Z`) |
| Lowercase | At least one ASCII lowercase letter (`a`–`z`) |
| Numbers | At least one ASCII digit (`0`–`9`) |
| Symbols | At least one symbol from Python's `string.punctuation`, such as `!`, `@`, `#`, or `_` |

Whitespace does not count as a symbol. Each satisfied rule contributes one point.

The assignment does not specify score thresholds, so this program uses:

| Score | Strength |
| --- | --- |
| 5 | Strong |
| 3–4 | Moderate |
| 0–2 | Weak |

These are educational rules, not a complete estimate of real-world password strength. The program does not save or transmit passwords.

## How to Run

Open a terminal in the project folder and run:

```bash
python password_checker.py
```

On systems that use `python3`, run `python3 password_checker.py` instead. No extra packages are required.

Enter a password to check it, or type `exit` to quit. After each result, enter `y` to check another password or `n` to finish. A blank password is assessed as Weak.

## Sample Input and Output

```text
=== Password Strength Checker ===
Enter your password (or type 'exit' to quit): Hello@123

Password Analysis:
Length: Satisfied
Uppercase: Satisfied
Lowercase: Satisfied
Numbers: Satisfied
Symbols: Satisfied
Password Strength: Strong
Do you want to check another password? (y/n): n
Thank you! Goodbye!
```

| Password | Satisfied rules | Score | Strength |
| --- | --- | --- | --- |
| `Hello@123` | Length, uppercase, lowercase, numbers, symbols | 5 | Strong |
| `Abc123` | Uppercase, lowercase, numbers | 3 | Moderate |
| `password` | Length, lowercase | 2 | Weak |

The eight-character minimum applies consistently: `Abc123` has 6 characters and fails the length check; `password` has 8 characters and passes it.

## Output Previews

These images are rendered captures of program runs.

### Strong Password

![Strong password output](Screenshots/01-strong-password.png)

### Moderate Password

![Moderate password output](Screenshots/02-moderate-password.png)

### Weak Password

![Weak password output](Screenshots/03-weak-password.png)

## Tests

```bash
python -m unittest discover -s tests -v
```

## Tech Used

- Python 3.
- Python standard library: `string` and `unittest`.
