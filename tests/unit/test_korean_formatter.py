import pytest

from cur.core.entity import Currency
from cur.utils.formatters.korean_formatter import format_korean


@pytest.mark.parametrize(
    "amount,currency,expected",
    [
        # Zero
        (0, Currency.KRW, "0원"),
        (0, Currency.USD, "0 달러"),
        (0, Currency.AUD, "0 달러"),
        # Small amounts with cents
        (1, Currency.USD, "1 달러"),
        (1.5, Currency.AUD, "1 달러 50 센트"),
        (13.55, Currency.AUD, "13 달러 55 센트"),
        (64.92, Currency.USD, "64 달러 92 센트"),
        (100, Currency.USD, "100 달러"),
        (999.99, Currency.AUD, "999 달러 99 센트"),
        # KRW (no cents)
        (100, Currency.KRW, "100원"),
        (999, Currency.KRW, "999원"),
        # 만 (10,000) - KRW
        (10_000, Currency.KRW, "1만원"),
        (15_000, Currency.KRW, "1만 5,000원"),
        (50_000, Currency.KRW, "5만원"),
        # 만 (10,000) - USD/AUD with cents
        (15_000, Currency.USD, "1만 5,000 달러"),
        (15_000.50, Currency.USD, "1만 5,000 달러 50 센트"),
        (50_000.99, Currency.AUD, "5만 달러 99 센트"),
        (50_000.987, Currency.AUD, "5만 달러 99 센트"),
        (50_000.987, Currency.USD, "5만 달러 99 센트"),
        # Thousand with cents
        (2457.65, Currency.AUD, "2,457 달러 65 센트"),
        (2457, Currency.AUD, "2,457 달러"),
        # 억 (100,000,000)
        (100_000_000, Currency.KRW, "1억원"),
        (150_000_000, Currency.USD, "1억 5,000만 달러"),
        (150_000_000.75, Currency.USD, "1억 5,000만 달러 75 센트"),
        (500_000_000, Currency.AUD, "5억 달러"),
        # 조 (1,000,000,000,000)
        (1_000_000_000_000, Currency.KRW, "1조원"),
        (1_500_000_000_000, Currency.USD, "1조 5,000억 달러"),
        (1_500_000_000_000.25, Currency.AUD, "1조 5,000억 달러 25 센트"),
        # Complex
        (1_385_000, Currency.KRW, "138만 5,000원"),
        (138_500_000, Currency.USD, "1억 3,850만 달러"),
        (138_500_000.50, Currency.USD, "1억 3,850만 달러 50 센트"),
        # Edge cases
        (53.45, Currency.AUD, "53 달러 45 센트"),
        (2458.7, Currency.AUD, "2,458 달러 70 센트"),
        (3470.9, Currency.USD, "3,470 달러 90 센트"),
    ],
)
def test_format_korean_parametrized(amount, currency, expected):
    output = format_korean(amount, currency)
    assert output == expected
