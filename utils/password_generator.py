import random
import string


def password_generator(length: int = 12) -> str:
    """Generate a strong random password."""
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    special = '!@#$%'

    # Guarantee at least one of each type
    password = [
        random.choice(uppercase),
        random.choice(lowercase),
        random.choice(digits),
        random.choice(special),
    ]
    all_chars = uppercase + lowercase + digits + special
    password += random.choices(all_chars, k=length - 4)
    random.shuffle(password)
    return ''.join(password)
