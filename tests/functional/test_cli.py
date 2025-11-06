from unittest.mock import Mock, patch

import pytest
from typer.testing import CliRunner

from cur.entrypoints.cli import app
from cur.services.conversion import ConversionResult


@pytest.fixture
def runner():
    """Create a CLI test runner."""
    return CliRunner()


@pytest.fixture
def mock_service():
    """Create a mock ConversionService."""
    return Mock()


def test_basic_conversion_usd_to_krw(runner, mock_service):
    """Test basic USD to KRW conversion."""
    mock_service.convert.return_value = ConversionResult(
        base_amount=1000.0,
        base_currency="USD",
        target_amount=1385000.0,
        target_currency="KRW",
        exchange_rate=1385.0,
    )

    with patch("cur.entrypoints.cli.bootstrap", return_value=mock_service):
        result = runner.invoke(app, ["1000", "usd", "krw"])

    assert result.exit_code == 0

    lines = result.stdout.strip().split("\n")
    assert len(lines) == 4, "Should have exactly 4 lines of output"

    assert "1,000 USD" in lines[0]
    assert "→" in lines[0]
    assert "1,385,000 KRW" in lines[0]

    assert "138만 5,000원" in lines[1]
    assert "1.4M" in lines[1]

    assert "Rate:" in lines[2]
    assert "1 USD" in lines[2]
    assert "1385" in lines[2]
    assert "KRW" in lines[2]

    assert lines[3] == "✓ Copied: 1,385,000"


def test_basic_conversion_krw_to_usd(runner, mock_service):
    """Test basic KRW to USD conversion."""
    mock_service.convert.return_value = ConversionResult(
        base_amount=50000.0,
        base_currency="KRW",
        target_amount=36.1,
        target_currency="USD",
        exchange_rate=0.000722,
    )

    with patch("cur.entrypoints.cli.bootstrap", return_value=mock_service):
        result = runner.invoke(app, ["50000", "krw", "usd"])

    assert result.exit_code == 0
    assert "50,000 KRW" in result.stdout
    assert "36.1 USD" in result.stdout
    assert "달러" in result.stdout
    assert "✓ Copied:" in result.stdout


def test_conversion_with_k_unit(runner, mock_service):
    """Test conversion with K unit (thousand)."""
    mock_service.convert.return_value = ConversionResult(
        base_amount=1500.0,
        base_currency="USD",
        target_amount=2077500.0,
        target_currency="KRW",
        exchange_rate=1385.0,
    )

    with patch("cur.entrypoints.cli.bootstrap", return_value=mock_service):
        result = runner.invoke(app, ["1.5k", "usd", "krw"])

    assert result.exit_code == 0
    assert "1,500 USD" in result.stdout
    assert "KRW" in result.stdout


def test_conversion_with_m_unit(runner, mock_service):
    """Test conversion with M unit (million)."""
    mock_service.convert.return_value = ConversionResult(
        base_amount=2300000.0,
        base_currency="KRW",
        target_amount=1660.65,
        target_currency="USD",
        exchange_rate=0.000722,
    )

    with patch("cur.entrypoints.cli.bootstrap", return_value=mock_service):
        result = runner.invoke(app, ["2.3M", "krw", "usd"])

    assert result.exit_code == 0
    assert "2,300,000 KRW" in result.stdout


def test_copy_format_default(runner, mock_service):
    """Test default copy format (with commas)."""
    mock_service.convert.return_value = ConversionResult(
        base_amount=1000.0,
        base_currency="USD",
        target_amount=1385000.0,
        target_currency="KRW",
        exchange_rate=1385.0,
    )

    with patch("cur.entrypoints.cli.bootstrap", return_value=mock_service):
        result = runner.invoke(app, ["1000", "usd", "krw"])

    assert result.exit_code == 0
    assert "✓ Copied: 1,385,000" in result.stdout


def test_copy_format_plain(runner, mock_service):
    """Test --copy plain option."""
    mock_service.convert.return_value = ConversionResult(
        base_amount=1000.0,
        base_currency="USD",
        target_amount=1385000.0,
        target_currency="KRW",
        exchange_rate=1385.0,
    )

    with patch("cur.entrypoints.cli.bootstrap", return_value=mock_service):
        result = runner.invoke(app, ["1000", "usd", "krw", "--copy", "plain"])

    assert result.exit_code == 0
    assert "✓ Copied: 1385000" in result.stdout


def test_copy_format_short(runner, mock_service):
    """Test --copy short option."""
    mock_service.convert.return_value = ConversionResult(
        base_amount=1000.0,
        base_currency="USD",
        target_amount=1385000.0,
        target_currency="KRW",
        exchange_rate=1385.0,
    )

    with patch("cur.entrypoints.cli.bootstrap", return_value=mock_service):
        result = runner.invoke(app, ["1000", "usd", "krw", "-c", "short"])

    assert result.exit_code == 0
    assert "✓ Copied:" in result.stdout
    assert "M" in result.stdout


def test_invalid_amount(runner):
    """Test invalid amount input."""
    result = runner.invoke(app, ["abc", "usd", "krw"])

    assert result.exit_code == 1
    assert "Error:" in result.stdout
    assert "Invalid amount format" in result.stdout


def test_invalid_currency(runner):
    """Test invalid currency input."""
    result = runner.invoke(app, ["1000", "usd", "eur"])

    assert result.exit_code == 1
    assert "Error:" in result.stdout
    assert "Unsupported currency" in result.stdout


def test_zero_amount(runner):
    """Test zero amount input."""
    result = runner.invoke(app, ["0", "usd", "krw"])

    assert result.exit_code == 1
    assert "Error:" in result.stdout
    assert "must be greater than zero" in result.stdout


def test_decimal_amount(runner, mock_service):
    """Test decimal amount input."""
    mock_service.convert.return_value = ConversionResult(
        base_amount=1234.56,
        base_currency="USD",
        target_amount=1709865.6,
        target_currency="KRW",
        exchange_rate=1385.0,
    )

    with patch("cur.entrypoints.cli.bootstrap", return_value=mock_service):
        result = runner.invoke(app, ["1234.56", "usd", "krw"])

    assert result.exit_code == 0
    assert "1,234.56 USD" in result.stdout
    assert "KRW" in result.stdout


def test_help_command(runner):
    """Test --help command."""
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Convert currency between AUD, KRW, and USD" in result.stdout
    assert "Amount to convert" in result.stdout
    assert "--copy" in result.stdout


def test_exact_output_format(runner, mock_service):
    """Test the exact output format matches expected structure."""
    mock_service.convert.return_value = ConversionResult(
        base_amount=1000.0,
        base_currency="USD",
        target_amount=1385000.0,
        target_currency="KRW",
        exchange_rate=1385.0,
    )

    with patch("cur.entrypoints.cli.bootstrap", return_value=mock_service):
        result = runner.invoke(app, ["1000", "usd", "krw"])

    assert result.exit_code == 0

    expected_output = (
        "1,000 USD → 1,385,000 KRW\n"
        "138만 5,000원 (1.4M)\n"
        "Rate: 1 USD = 1385.0 KRW\n"
        "✓ Copied: 1,385,000\n"
    )
    assert result.stdout == expected_output


def test_service_called_with_correct_parameters(runner, mock_service):
    """Test that the service is called with correct parsed parameters."""
    mock_service.convert.return_value = ConversionResult(
        base_amount=1000.0,
        base_currency="USD",
        target_amount=1385000.0,
        target_currency="KRW",
        exchange_rate=1385.0,
    )

    with patch("cur.entrypoints.cli.bootstrap", return_value=mock_service):
        result = runner.invoke(app, ["1000", "usd", "krw"])

    assert result.exit_code == 0

    # Verify service.convert was called once
    assert mock_service.convert.call_count == 1

    # Verify arguments
    call_args = mock_service.convert.call_args[0]
    assert call_args[0] == 1000.0  # parsed amount
    assert call_args[1].code == "USD"  # from_currency
    assert call_args[2].code == "KRW"  # to_currency
