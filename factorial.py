def factorial(number):
    if number < 0:
        raise ValueError("Factorial is not defined for negative numbers.")

    result = 1
    for value in range(2, number + 1):
        result *= value
    return result


def main():
    try:
        number = int(input("Enter a number: "))
    except ValueError:
        print("Please enter a whole number.")
        return 1
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled.")
        return 1

    try:
        result = factorial(number)
    except ValueError as error:
        print(error)
        return 1

    print(f"Factorial of {number} = {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
