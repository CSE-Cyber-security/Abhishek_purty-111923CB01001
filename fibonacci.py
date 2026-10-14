def fibonacci(count):
    if count <= 0:
        raise ValueError("Please enter a positive number of terms.")

    series = []
    first, second = 0, 1
    for _ in range(count):
        series.append(first)
        first, second = second, first + second
    return series


def main():
    try:
        count = int(input("Enter number of terms: "))
    except ValueError:
        print("Please enter a whole number.")
        return 1
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled.")
        return 1

    try:
        series = fibonacci(count)
    except ValueError as error:
        print(error)
        return 1

    print("Fibonacci series:", *series)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
