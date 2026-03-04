import re

_ALPHA_RE = re.compile(r"[A-Za-z]+")

def _letters_only(token: str) -> str:
    m = _ALPHA_RE.findall(token or "")
    return "".join(m)

def make_prefix(client_name: str) -> str:
    name = (client_name or "").strip()
    parts = [p for p in re.split(r"\s+", name) if p]
    parts_clean = [_letters_only(p) for p in parts]
    parts_clean = [p for p in parts_clean if p]

    prefix = ""
    if len(parts_clean) >= 2:
        # first letter of first 3 words
        for w in parts_clean[:3]:
            if w:
                prefix += w[0]
    else:
        # single word => first 3 letters
        word = parts_clean[0] if parts_clean else ""
        prefix = word[:3]

    prefix = prefix.upper()

    # pad to 3 with A-Z starting from A
    pad_char = ord("A")
    while len(prefix) < 3:
        prefix += chr(pad_char)
        pad_char += 1
        if pad_char > ord("Z"):
            pad_char = ord("A")

    return prefix[:3]

def format_code(prefix: str, number: int) -> str:
    return f"{prefix}{number:03d}"
