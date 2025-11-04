import pytest

from cur.utils.formatters.number_formatter import (
    format_plain,
    format_short,
    format_with_commas,
)


@pytest.mark.parametrize(
    "input, expected",
    [
        (1_000_000, "1,000,000"),
        (1452.67, "1,452.67"),
        (1234.5678, "1,234.57"),
        (1234.00, "1,234"),
    ],
)
def test_format_with_commas(input: float, expected: str):
    output = format_with_commas(input)

    assert output == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        (1_000_000, "1000000"),
        (1452.67, "1452.67"),
        (1234.5678, "1234.57"),
        (1234.00, "1234"),
    ],
)
def test_format_plain(input: float, expected: str):
    output = format_plain(input)

    assert output == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        (1_000_000_000, "1B"),
        (1_000_000, "1M"),
        (1_234_000, "1.2M"),
        (1_260_000, "1.3M"),
        (1234.00, "1.2K"),
        (1234.5678, "1.2K"),
        (1452.67, "1.5K"),
        (100.00, "100"),
    ],
)
def test_format_short(input: float, expected: str):
    output = format_short(input)

    assert output == expected
