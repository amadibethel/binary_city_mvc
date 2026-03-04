import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def required(value: str) -> bool:
    return value is not None and str(value).strip() != ""

def is_email(value: str) -> bool:
    if value is None:
        return False
    return EMAIL_RE.match(value.strip()) is not None
