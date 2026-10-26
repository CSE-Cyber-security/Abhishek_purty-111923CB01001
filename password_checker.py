import string


def analyze_password(password):
    checks = {
        "Length": len(password) >= 8,
        "Uppercase": False,
        "Lowercase": False,
        "Numbers": False,
        "Symbols": False,
    }

    for character in password:
        if "A" <= character <= "Z":
            checks["Uppercase"] = True
        elif "a" <= character <= "z":
            checks["Lowercase"] = True
        elif "0" <= character <= "9":
            checks["Numbers"] = True
        elif character in string.punctuation:
            checks["Symbols"] = True

    score = sum(checks.values())
    if score == 5:
        strength = "Strong"
    elif score >= 3:
        strength = "Moderate"
    else:
        strength = "Weak"

    return checks, strength


def display_analysis(password):
    checks, strength = analyze_password(password)
    print("\nPassword Analysis:")
    for criterion, satisfied in checks.items():
        status = "Satisfied" if satisfied else "Not satisfied"
        print(f"{criterion}: {status}")
    print(f"Password Strength: {strength}")


def main():
    print("=== Password Strength Checker ===")

    try:
        while True:
            password = input("Enter your password (or type 'exit' to quit): ")
            if password.lower() == "exit":
                break

            display_analysis(password)

            while True:
                answer = input("Do you want to check another password? (y/n): ").strip().lower()
                if answer in ("y", "n", "exit"):
                    break
                print("Please enter y or n.")

            if answer != "y":
                break
            print()
    except (EOFError, KeyboardInterrupt):
        print()

    print("Thank you! Goodbye!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
