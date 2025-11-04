import pytest

from cur.core.entity import Currency
from cur.utils.formatters.korean_formatter import format_korean


@pytest.mark.parametrize(
    "amount,currency,expected",
    [
        # Zero
        (0, Currency.KRW, "0원"),
        (0, Currency.USD, "0 미국 달러"),
        # Decimals < 1
        (0.5, Currency.USD, "0.50 미국 달러"),
        (0.99, Currency.KRW, "0.99원"),
        # Small (1~999)
        (1, Currency.USD, "1 미국 달러"),
        (100, Currency.KRW, "100원"),
        (999, Currency.AUD, "999 호주 달러"),
        # 만 (10,000)
        (10_000, Currency.KRW, "1만원"),
        (15_000, Currency.USD, "1만 5,000 미국 달러"),
        (50_000, Currency.AUD, "5만 호주 달러"),
        # 억 (100,000,000)
        (100_000_000, Currency.KRW, "1억원"),
        (150_000_000, Currency.USD, "1억 5,000만 미국 달러"),
        (500_000_000, Currency.AUD, "5억 호주 달러"),
        # 조 (1,000,000,000,000)
        (1_000_000_000_000, Currency.KRW, "1조원"),
        (1_500_000_000_000, Currency.USD, "1조 5,000억 미국 달러"),
        # Complex
        (1_385_000, Currency.KRW, "138만 5,000원"),
        (138_500_000, Currency.USD, "1억 3,850만 미국 달러"),
        (1_234_567_890, Currency.AUD, "12억 3,456만 7,890 호주 달러"),
    ],
)
def test_format_korean_parametrized(amount, currency, expected):
    output = format_korean(amount, currency)
    assert output == expected
