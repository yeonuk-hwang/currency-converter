from cur.core.entity import Currency


def format_korean(amount: float, currency: Currency) -> str:
    if currency.subunit_name:
        return _format_with_subunit(amount, currency)
    else:
        return _format_only_main_unit(amount, currency)


def _format_only_main_unit(amount: float, currency: Currency) -> str:
    unit = currency.korean_name

    if amount == 0:
        return f"0{unit}"

    if amount < 1000:
        return f"{int(round(amount)):,d}{unit}"

    parts = []

    num = int(round(amount))

    if num >= 1_000_000_000_000:
        jo = num // 1_000_000_000_000
        rest = num % 1_000_000_000_000
        parts.append(f"{jo:,d}조")
        num = rest

    if num >= 100_000_000:
        eok = num // 100_000_000
        rest = num % 100_000_000
        parts.append(f"{eok:,d}억")
        num = rest

    if num >= 10_000:
        man = num // 10_000
        rest = num % 10_000
        parts.append(f"{man:,d}만")
        num = rest

    if num > 0:
        parts.append(f"{num:,d}")

    korean_formatted = " ".join(parts)

    return f"{korean_formatted}{unit}"


def _format_with_subunit(amount: float, currency: Currency) -> str:
    main_unit = currency.korean_name
    subunit = currency.subunit_name

    integer_part = int(amount)
    decimal_part = round((amount - integer_part) * 100)

    parts = []

    if integer_part > 0:
        if integer_part < 1000:
            parts.append(f"{integer_part:,d} {main_unit}")
        else:
            korean_parts = []
            num = integer_part

            if num >= 1_000_000_000_000:
                jo = num // 1_000_000_000_000
                rest = num % 1_000_000_000_000
                korean_parts.append(f"{jo:,d}조")
                num = rest

            if num >= 100_000_000:
                eok = num // 100_000_000
                rest = num % 100_000_000
                korean_parts.append(f"{eok:,d}억")
                num = rest

            if num >= 10_000:
                man = num // 10_000
                rest = num % 10_000
                korean_parts.append(f"{man:,d}만")
                num = rest

            if num > 0:
                korean_parts.append(f"{num:,d}")

            parts.append(f"{' '.join(korean_parts)} {main_unit}")

    if decimal_part > 0:
        parts.append(f"{decimal_part} {subunit}")

    if not parts:
        return f"0 {main_unit}"

    return " ".join(parts)
