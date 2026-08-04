import re


def safe_text(text: str) -> str:
    # ignore - заставляет игнорировать байты недопустимые для этой кодировки
    return text.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")


def sanitize_input(text: str, max_length: int = 1000) -> tuple[str, list[str]]:
    changes = []
    sanitized = text

    # удаление нулевые байты, т.к их не очень могут воспринимать другие форматы
    if "\x00" in sanitized:
        sanitized = sanitized.replace("\x00", "")
        changes.append("removed null bytes")

    escaped_hex = re.sub(r"\\x[0-9a-fA-F]{2}", "", sanitized)

    # удаление \x00
    if escaped_hex != sanitized:
        sanitized = escaped_hex
        changes.append("removed escaped hex bytes")

    # удаление пробелов
    stripped = sanitized.strip()
    if stripped != sanitized:
        sanitized = stripped
        changes.append("trimmed whitespace")

    # \s+ - удаление лишних пробелов
    # \s - пробле, таб, \n, \t
    collapsed = re.sub(
        r"\s+", " ", sanitized
    )  # замена пробелов на "" из строки sanitized
    if collapsed != sanitized:
        sanitized = collapsed
        changes.append("collapsed whitespace")

    cleaned = sanitized.encode("utf-8", errors="ignore").decode(
        "utf-8", errors="ignore"
    )  # удаление битых unicode символов или непонятных символов
    if cleaned != sanitized:
        sanitized = cleaned
        changes.append("removed invalid unicode characters")

    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
        changes.append(f"truncated to {max_length} chars")

    return sanitized, changes
