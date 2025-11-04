import pytest

from cur.core.entity import Currency
from cur.core.exception import ParseError
from cur.services.parser import parse_amount, parse_currency


class TestParseAmount:
    def test_parse_plain_integer(self):
        assert parse_amount("1000") == 1000.0
        assert parse_amount("42") == 42.0
        assert parse_amount("1") == 1.0

    def test_parse_plain_decimal(self):
        assert parse_amount("1234.56") == 1234.56
        assert parse_amount("0.5") == 0.5
        assert parse_amount(".75") == 0.75

    def test_parse_with_commas(self):
        assert parse_amount("1,000") == 1_000.0
        assert parse_amount("1,000,000") == 1_000_000.0
        assert parse_amount("10,000.50") == 10_000.5
        assert parse_amount("1,234,567.89") == 1_234_567.89

    def test_parse_k_unit(self):
        assert parse_amount("1k") == 1_000.0
        assert parse_amount("1K") == 1_000.0
        assert parse_amount("1.5k") == 1_500.0
        assert parse_amount("2.5K") == 2_500.0
        assert parse_amount("0.5k") == 500.0

    def test_parse_k_unit_with_commas(self):
        assert parse_amount("1,500k") == 1_500_000.0  # 1.5M
        assert parse_amount("2,300K") == 2_300_000.0  # 2.3M

    def test_parse_m_unit(self):
        assert parse_amount("1m") == 1_000_000.0
        assert parse_amount("1M") == 1_000_000.0
        assert parse_amount("2.3m") == 2_300_000.0
        assert parse_amount("0.5M") == 500_000.0

    def test_parse_b_unit(self):
        assert parse_amount("1b") == 1_000_000_000.0
        assert parse_amount("1B") == 1_000_000_000.0
        assert parse_amount("1.5b") == 1_500_000_000.0
        assert parse_amount("0.1B") == 100_000_000.0

    def test_parse_with_whitespace(self):
        assert parse_amount("  1000  ") == 1000.0
        assert parse_amount("  1.5k  ") == 1_500.0
        assert parse_amount("  1,000  ") == 1_000.0

    def test_parse_case_insensitive(self):
        assert parse_amount("1k") == parse_amount("1K")
        assert parse_amount("1m") == parse_amount("1M")
        assert parse_amount("1b") == parse_amount("1B")

    def test_parse_zero(self):
        with pytest.raises(ParseError, match="Amount must be greater than zero"):
            parse_amount("0")

        with pytest.raises(ParseError, match="Amount must be greater than zero"):
            parse_amount("0.0")

    def test_parse_empty_string(self):
        """Test parsing empty string raises error."""
        with pytest.raises(ParseError, match="Amount cannot be empty"):
            parse_amount("")

        with pytest.raises(ParseError, match="Amount cannot be empty"):
            parse_amount("   ")

    def test_parse_invalid_format(self):
        with pytest.raises(ParseError, match="Invalid amount format"):
            parse_amount("abc")

        with pytest.raises(ParseError, match="Invalid amount format"):
            parse_amount("1.2.3")

        with pytest.raises(ParseError, match="Invalid amount format"):
            parse_amount("1x")

    def test_no_negative_numbers(self):
        with pytest.raises(ParseError, match="Invalid amount format"):
            parse_amount("-1000")

        with pytest.raises(ParseError, match="Invalid amount format"):
            parse_amount("+1000")

        with pytest.raises(ParseError, match="Invalid amount format"):
            parse_amount("-1.5k")


class TestParseCurrency:
    def test_parse_valid_currencies(self):
        assert parse_currency("usd") == Currency.USD
        assert parse_currency("USD") == Currency.USD
        assert parse_currency("krw") == Currency.KRW
        assert parse_currency("KRW") == Currency.KRW
        assert parse_currency("aud") == Currency.AUD
        assert parse_currency("AUD") == Currency.AUD

    def test_parse_with_whitespace(self):
        assert parse_currency("  usd  ") == Currency.USD
        assert parse_currency("  KRW  ") == Currency.KRW

    def test_parse_invalid_currency(self):
        with pytest.raises(ParseError, match="Unsupported currency: EUR"):
            parse_currency("EUR")

        with pytest.raises(ParseError, match="Unsupported currency: JPY"):
            parse_currency("JPY")

        with pytest.raises(ParseError, match="Unsupported currency: ABC"):
            parse_currency("abc")

    def test_error_message_includes_supported_currencies(self):
        with pytest.raises(ParseError, match="Supported: AUD, KRW, USD"):
            parse_currency("GBP")
