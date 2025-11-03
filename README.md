## Project Overview

A command-line interface tool for quick currency conversion between AUD, KRW, and USD. Originally built to replace broken Alfred workflow, this tool is designed for fast access via Ghostty's quick terminal feature with simple, intuitive commands.

## Functional Requirements

1. Currency Conversion Logic

Input: A numeric amount and a source currency code (AUD, KRW, or USD)
Output: Converted amounts in the two other currencies

When AUD is input → Display results in KRW and USD
When KRW is input → Display results in AUD and USD
When USD is input → Display results in AUD and KRW

2. Dual Number Formatting
   Each converted amount must be displayed in two formats:

Numeric format: Standard number with appropriate decimal places and thousand separators

Example: 1,234,567.89 or 1,234,567

Korean semantic format: Human-readable Korean units

억 (eok) = 100,000,000 (hundred million)
만 (man) = 10,000 (ten thousand)
Examples:

150,000,000 → "1.5억"
5,000,000 → "500만"
35,000 → "3.5만"

3. Exchange Rate Information

Display current exchange rates used for conversion
Format: "1 [SOURCE] = [RATE] [TARGET]"
Example: "1 AUD = 900.5 KRW"
Exchange rates must be fetched from a reliable, real-time API

4. Real-time Exchange Rates

Use a currency exchange rate API (e.g., exchangerate-api.com, fixer.io)
Implement caching mechanism to avoid excessive API calls

Cache duration: 12-24 hours recommended
Cache location: User's home directory (e.g., ~/.cache/currency-translator/)

Gracefully handle API failures with informative error messages

5. Command-line Interface

Command format: cx <amount> <currency>
Examples:

bash cx 1000 aud
cx 1000000 krw
cx 500 usd

Case-insensitive currency codes (AUD, aud, Aud should all work)
Input validation:

Amount must be a valid number (integer or decimal)
Currency must be one of: AUD, KRW, USD
Display helpful error messages for invalid inputs

6. Standalone Executable

Must run directly from terminal without requiring runtime interpreters
No need to prefix with python, node, or similar commands
Should work as a system-wide command after installation
For Python: Package as executable via pipx, uv, or PyInstaller
For Go: Compile to single binary that can be placed in PATH

Non-Functional Requirements

1. Performance

Fast startup time (< 1 second)
Minimal latency for conversions
Efficient caching to reduce API calls

2. User Experience

Clean, readable output formatting
Use colors and tables for better readability
Clear error messages with usage examples
Intuitive command structure

3. Reliability

Handle network failures gracefully
Validate API responses
Provide fallback behavior when API is unavailable
Cache validation to ensure data freshness

4. Cross-platform Compatibility

Must work on macOS (primary target for Ghostty integration)
Bonus: Linux and Windows compatibility

5. Maintainability

Clean, well-documented code
Modular architecture for easy updates
Simple configuration for API endpoints

Technical Specifications
Input Validation Rules

Amount must be a positive number
Currency code must be exactly 3 characters
Currency code must be one of the supported currencies
Invalid inputs should show usage help

Output Format Specification
💰 [AMOUNT] [SOURCE_CURRENCY]

┌──────────┬────────────────────┬──────────────┬─────────────────────────┐
│ 통화 │ 금액 │ 한글 표기 │ 환율 │
├──────────┼────────────────────┼──────────────┼─────────────────────────┤
│ KRW │ 1,350,750 KRW │ 135.1만 │ 1 AUD = 900.50 KRW │
│ USD │ 0.67 USD │ 0.67 │ 1 AUD = 0.6700 USD │
└──────────┴────────────────────┴──────────────┴─────────────────────────┘
Number Formatting Rules

KRW: No decimal places (whole numbers only)
AUD/USD: 2 decimal places
Thousand separators: Use commas (,)
Korean format:

= 100,000,000: Display as "X.X억"

= 10,000: Display as "X.X만"

= 1,000: Display with thousand separators

< 1,000: Display with 2 decimal places

Caching Strategy

Cache file location: ~/.cache/currency-translator/rates.json
Cache structure:

json {
"timestamp": "2025-11-04T10:30:00",
"base": "AUD",
"rates": {
"KRW": 900.5,
"USD": 0.67,
...
}
}

Check cache validity before API call
Update cache after successful API response

Installation Requirements
Python Version

Use pipx or uv for installation
Command after install: cx
Dependencies managed via pyproject.toml

Go Version

Compile to single binary
Install by copying to system PATH
No external dependencies at runtime

Integration with Ghostty Quick Terminal

The command must execute quickly (< 1 second total)
Output should be concise but complete
Support being called repeatedly without issues
Clean exit codes for scripting

Future Enhancements (Optional)

Support for additional currencies
Historical exchange rate comparisons
Reverse calculation (from target currency)
Configuration file for custom API keys
Output in different formats (JSON, CSV)
Currency symbol display

Success Criteria

✅ Converts between AUD, KRW, USD accurately
✅ Displays both numeric and Korean semantic formats
✅ Shows current exchange rates
✅ Works as standalone command without interpreter prefix
✅ Fast execution (< 1 second)
✅ Reliable caching mechanism
✅ Clear, readable output
✅ Proper error handling and validation
