# password_generator.py

import secrets
import string


def generate_password(length, use_uppercase, use_digits, use_symbols):
    if length < 4:
        raise ValueError("Password length must be at least 4.")

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%^&*()-_=+?"

    characters = lowercase
    required = [secrets.choice(lowercase)]

    if use_uppercase:
        characters += uppercase
        required.append(secrets.choice(uppercase))

    if use_digits:
        characters += digits
        required.append(secrets.choice(digits))

    if use_symbols:
        characters += symbols
        required.append(secrets.choice(symbols))

    if length < len(required):
        raise ValueError("Password length is too short for selected options.")

    remaining = [
        secrets.choice(characters)
        for _ in range(length - len(required))
    ]

    password = required + remaining
    secrets.SystemRandom().shuffle(password)

    return "".join(password)


def main():
    print("=" * 35)
    print("       PASSWORD GENERATOR")
    print("=" * 35)

    while True:
        try:
            length = int(input("Enter password length (4-64): "))
            if 4 <= length <= 64:
                break
            print("Please enter a length between 4 and 64.")
        except ValueError:
            print("Please enter a valid number.")

    uppercase = input("Include uppercase letters? (y/n): ").strip().lower() == "y"
    digits = input("Include numbers? (y/n): ").strip().lower() == "y"
    symbols = input("Include symbols? (y/n): ").strip().lower() == "y"

    password = generate_password(length, uppercase, digits, symbols)

    print("\nYour generated password is:")
    print(password)

    again = input("\nGenerate another password? (y/n): ").strip().lower()
    if again == "y":
        print()
        main()
    else:
        print("Thank you for using Password Generator!")


if __name__ == "__main__":
    main()
