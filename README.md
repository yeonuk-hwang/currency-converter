## Project Overview

A command-line interface tool for quick currency conversion between AUD, KRW, and USD. Originally built to replace broken Alfred workflow, this tool is designed for fast access via Ghostty's quick terminal feature with simple, intuitive commands.

## Key Features

**🎨 Smart Output Formatting**

- **Multi-format display**: Shows results in numbers, Korean text (한글), and short units (K/M/B) simultaneously
- Example: `1,385,000 KRW` → `138만 5천원 (1.39M)`
- Makes it easy to understand amounts in different representations at a glance

**⌨️ Flexible Input Options**

- **Comma-separated numbers**: `1,000`, `1,000,000` for better readability
- **Unit suffixes**: `1.5K` (thousand), `2.3M` (million), `1.5B` (billion)
- **Case-insensitive**: `1k`, `1K`, `1.5m`, `1.5M` all work
- **Decimal support**: `1234.56`, `1.5k`

## Installation

### Using uv (Recommended)

```bash
# Install from the current directory
uv tool install .

# Or install in editable mode for development
uv tool install --editable .
```

### Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager

### Development

```bash
# Run directly without installation (recommended for development)
uv run cur 100 usd krw

# Run tests
uv run pytest

# Install dependencies
uv sync
```

## Usage

### Basic Currency Conversion

```bash
# Convert between any supported currencies (AUD, KRW, USD)
$ cur 1000 usd krw
1,000 USD → 1,385,000 KRW
138만 5천원 (1.39M)
Rate: 1 USD = 1.385 KRW
✓ Copied: 1,385,000

$ cur 50000 krw aud
50,000 KRW → 54.25 AUD
54달러 25센트 (54.25)
Rate: 1 KRW = 0.001085 AUD
✓ Copied: 54.25

$ cur 100 aud usd
100 AUD → 65.13 USD
65달러 13센트 (65.13)
Rate: 1 AUD = 0.6513 USD
✓ Copied: 65.13

```

### Input with K/M/B Units

```bash
# Use K (thousand), M (million), B (billion) - case insensitive
$ cur 1.5k usd krw
1,500 USD → 2,077,500 KRW
207만 7천 5백원 (2.08M)
Rate: 1 USD = 1.385 KRW
✓ Copied: 2,077,500

$ cur 2.3M krw aud
2,300,000 KRW → 2,555.56 AUD
2천 5백 55달러 56센트 (2.56K)
Rate: 1 KRW = 0.001085 AUD
✓ Copied: 2,555.56

$ cur 1.5B aud usd
1,500,000,000 AUD → 976,500,000 USD
9억 7천 6백 50만 달러 (976.5M)
Rate: 1 AUD = 0.6513 USD
✓ Copied: 976,500,000

# Decimal inputs also supported
$ cur 1234.56 usd krw
1,234.56 USD → 1,709,865.60 KRW
170만 9천 8백 65원 (1.71M)
Rate: 1 USD = 1.385 KRW
✓ Copied: 1,709,865.60
```

### Copy options

```bash
# Default: Copy with commas
$ cur 1000 usd krw
1,000 USD → 1,385,000 KRW
138만 5천원 (1.39M)
Rate: 1 USD = 1.385 KRW
✓ Copied: 1,385,000

# Copy without commas
$ cur 1000 usd krw --copy plain
1,000 USD → 1,385,000 KRW
138만 5천원 (1.39M)
Rate: 1 USD = 1.385 KRW
✓ Copied: 1385000

# Copy in short format (K/M/B)
$ cur 1000 usd krw --copy short
1,000 USD → 1,385,000 KRW
138만 5천원 (1.39M)
Rate: 1 USD = 1.385 KRW
✓ Copied: 1.39M

# Short option flag
$ cur 5000000 krw usd -c short
5,000,000 KRW → 3,610.11 USD
3천 6백 10달러 (3.61K)
Rate: 1 KRW = 0.000722 USD
✓ Copied: 3.61K
```

## Exchange Rate Data

This tool uses the free API provided by [ExchangeRate-API](https://www.exchangerate-api.com/) for currency conversion rates.
