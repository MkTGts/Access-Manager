import secrets
import string


def generate_password(length=10):
    if length < 4:
        raise ValueError("Password length must be at least 4")
    
    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    
    # Ensure at least one of each type
    password = [
        secrets.choice(lowercase),
        secrets.choice(uppercase),
        secrets.choice(digits)
    ]
    
    # Fill the rest randomly
    all_chars = lowercase + uppercase + digits
    for _ in range(length - 3):
        password.append(secrets.choice(all_chars))
    
    # Shuffle the password
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)