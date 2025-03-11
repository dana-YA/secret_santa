import random
import string


def generate_password(
    length=12, use_uppercase=True, use_digits=True, use_special_chars=True
):
    """
    Generate a random password.

    :param length: Length of the password (default: 12).
    :param use_uppercase: Include uppercase letters (default: True).
    :param use_digits: Include digits (default: True).
    :param use_special_chars: Include special characters (default: True).
    :return: Randomly generated password.
    """
    # Define character sets
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase if use_uppercase else ""
    digits = string.digits if use_digits else ""
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?" if use_special_chars else ""

    # Combine character sets
    all_chars = lowercase_letters + uppercase_letters + digits + special_chars

    # Ensure at least one character from each selected set
    password = []
    if use_uppercase:
        password.append(random.choice(uppercase_letters))
    if use_digits:
        password.append(random.choice(digits))
    if use_special_chars:
        password.append(random.choice(special_chars))

    # Fill the rest of the password with random characters
    remaining_length = length - len(password)
    password.extend(random.choice(all_chars) for _ in range(remaining_length))

    # Shuffle to ensure randomness
    random.shuffle(password)

    # Convert list to string
    return "".join(password)
