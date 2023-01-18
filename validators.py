from email_validator import validate_email, EmailNotValidError


def is_valid_email(email: str):
    """Verifies the correctness of an email address"""
    try:
        # Check that the email address is valid.
        validate_email(email, check_deliverability=True)
        return True
    except EmailNotValidError:
        # Email is not valid.
        return False
