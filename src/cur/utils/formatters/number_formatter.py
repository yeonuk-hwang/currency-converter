def format_with_commas(number: float) -> str:
    return _remove_trailing_zeros(f"{number:,.2f}")


def format_plain(number: float) -> str:
    return _remove_trailing_zeros(f"{number:.2f}")


def format_short(number: float) -> str:
    result: str | None = None

    if number >= 1_000_000_000:
        value = number / 1_000_000_000
        result = f"{value:.1f}B"
    elif number >= 1_000_000:
        value = number / 1_000_000
        result = f"{value:.1f}M"
    elif number >= 1_000:
        value = number / 1_000
        result = f"{value:.1f}K"
    else:
        result = f"{number:.2f}"

    return _remove_trailing_zeros((result))


def _remove_trailing_zeros(formatted: str) -> str:
    """
    Remove unnecessary trailing zeros.

    Args:
        formatted: Formatted number string

    Returns:
        String with trailing zeros removed

    Examples:
        >>> remove_trailing_zeros("1.50M")
        '1.5M'
        >>> remove_trailing_zeros("1,385,000.00")
        '1,385,000'
    """
    if "." in formatted:
        # Split by suffix if exists (K/M/B)
        for suffix in ["K", "M", "B"]:
            if suffix in formatted:
                num_part, _ = formatted.split(suffix)
                num_part = num_part.rstrip("0").rstrip(".")
                return f"{num_part}{suffix}"

        # No suffix
        return formatted.rstrip("0").rstrip(".")

    return formatted
