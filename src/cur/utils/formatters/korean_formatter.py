from cur.core.entity import Currency


def format_korean(number: float, currency: Currency) -> str:
    unit = (
        currency.korean_name if currency == Currency.KRW else f" {currency.korean_name}"
    )

    if number == 0:
        return f"0{unit}"

    if number < 1:
        return f"{number:.2f}{unit}"

    if number < 1000:
        if number == int(number):
            return f"{int(number)}{unit}"
        else:
            return f"{number:.2f}{unit}"

    num = int(round(number))

    parts = []

    if num >= 1_000_000_000_000:
        jo = num // 1_000_000_000_000
        rest = num % 1_000_000_000_000
        parts.append(f"{jo:,}조")
        num = rest

    if num >= 100_000_000:
        eok = num // 100_000_000
        rest = num % 100_000_000
        parts.append(f"{eok:,}억")
        num = rest

    if num >= 10_000:
        man = num // 10_000
        rest = num % 10_000
        parts.append(f"{man:,}만")
        num = rest

    if num > 0:
        parts.append(f"{num:,}")

    korean_formatted = " ".join(parts)

    return f"{korean_formatted}{unit}"
