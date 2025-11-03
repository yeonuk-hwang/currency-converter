## Project Overview

A command-line interface tool for quick currency conversion between AUD, KRW, and USD. Originally built to replace broken Alfred workflow, this tool is designed for fast access via Ghostty's quick terminal feature with simple, intuitive commands.

## Usage

### Basic Currency Conversion

```bash
# Convert between any supported currencies (AUD, KRW, USD)
$ cur 1000 usd krw
1,000 USD = 1,385,000 KRW (138만 5천원) [1.39M]
✓ Copied: 1,385,000

$ cur 50000 krw aud
50,000 KRW = 54.25 AUD (54달러 25센트) [54.25]
✓ Copied: 54.25

$ cur 100 aud usd
100 AUD = 65.13 USD (65달러 13센트) [65.13]
✓ Copied: 65.13

```

### Input with K/M/B Units

```bash
# Use K (thousand), M (million), B (billion) - case insensitive
$ cur 1.5k usd krw
1,500 USD = 2,077,500 KRW (207만 7천 5백원) [2.08M KRW]
✓ Copied: 2,077,500

$ cur 2.3M krw aud
2,300,000 KRW = 2,555.56 AUD (2천 5백 55달러 56센트) [2.56K]
✓ Copied: 2,555.56

$ cur 1.5B aud usd
1,500,000,000 AUD = 976,500,000 USD (9억 7천 6백 50만 달러) [976.5M]
✓ Copied: 976,500,000

# Decimal inputs also supported
$ cur 1234.56 usd krw
1,234.56 USD = 1,709,865.60 KRW (170만 9천 8백 65원) [1.71M]
✓ Copied: 1,709,865.60
```

### Copy options

```bash
# Default: Copy with commas
$ cur 1000 usd krw
1,000 USD = 1,385,000 KRW (138만 5천원) [1.39M]
✓ Copied: 1,385,000

# Copy without commas
$ cur 1000 usd krw --copy plain
1,000 USD = 1,385,000 KRW (138만 5천원) [1.39M]
✓ Copied: 1385000

# Copy in short format (K/M/B)
$ cur 1000 usd krw --copy short
1,000 USD = 1,385,000 KRW (138만 5천원) [1.39M]
✓ Copied: 1.39M

# Short option flag
$ cur 5000000 krw usd -c short
5,000,000 KRW = 3,610.11 USD (3천 6백 10달러) [3.61K]
✓ Copied: 3.61K
```
