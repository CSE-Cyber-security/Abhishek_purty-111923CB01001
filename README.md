# Week 03 – Fibonacci Series

A Python program that prints the requested number of terms in the Fibonacci series.

## Problem Statement

The Fibonacci series starts with 0 and 1. Each following term is the sum of the previous two terms. This program takes the number of terms from the user and displays the series.

## How to Run

Open a terminal in the project folder and run:

```bash
python fibonacci.py
```

On systems that use `python3`, run `python3 fibonacci.py` instead.

Enter a positive whole number when prompted for the number of terms.

## Sample Input and Output

```text
Enter number of terms: 10
Fibonacci series: 0 1 1 2 3 5 8 13 21 34
```

## How It Works

The program starts with 0 and 1. A loop adds the current term to a list, then calculates the next term by adding the previous two values. The loop runs once for each requested term.

Zero, negative numbers, decimal values, and text inputs display an error message.

## Tech Used

- Python 3.
- No extra packages required.
