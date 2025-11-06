from enum import Enum

import typer
from rich.console import Console
from typing_extensions import Annotated

from cur.adapters.clipboard import copy
from cur.bootstrap import bootstrap
from cur.core.exception import ParseError
from cur.services.parser import parse_amount, parse_currency
from cur.utils.formatters.korean_formatter import format_korean
from cur.utils.formatters.number_formatter import (
    format_plain,
    format_short,
    format_with_commas,
)

app = typer.Typer(help="Quick currency conversion tool for AUD, KRW, and USD")
console = Console(highlighter=None)  # Disable automatic highlighting


class CopyFormat(str, Enum):
    default = "default"
    plain = "plain"
    short = "short"


@app.command()
def convert(
    amount: Annotated[
        str, typer.Argument(help="Amount to convert (supports K/M/B units)")
    ],
    from_currency: Annotated[str, typer.Argument(help="Source currency (AUD/KRW/USD)")],
    to_currency: Annotated[str, typer.Argument(help="Target currency (AUD/KRW/USD)")],
    copy_format: Annotated[
        CopyFormat,
        typer.Option(
            "--copy",
            "-c",
            help="Format for clipboard: default (with commas), plain (no commas), short (K/M/B)",
        ),
    ] = CopyFormat.default,
):
    """Convert currency between AUD, KRW, and USD."""
    try:
        # Parse inputs
        parsed_amount = parse_amount(amount)
        from_cur = parse_currency(from_currency)
        to_cur = parse_currency(to_currency)

        # Convert
        service = bootstrap()
        result = service.convert(parsed_amount, from_cur, to_cur)

        # Format amounts for display
        from_formatted = format_with_commas(result.base_amount)
        to_formatted = format_with_commas(result.target_amount)
        korean_formatted = format_korean(result.target_amount, to_cur)
        short_formatted = format_short(result.target_amount)

        # Display result
        console.print(
            f"[bold green]{from_formatted}[/bold green] [bold cyan]{result.base_currency}[/bold cyan] → "
            f"[bold green]{to_formatted}[/bold green] [bold cyan]{result.target_currency}[/bold cyan]"
        )
        console.print(
            f"[bold green]{korean_formatted}[/bold green] "
            f"([bold green]{short_formatted}[/bold green])"
        )
        console.print(
            f"Rate: 1 [bold cyan]{result.base_currency}[/bold cyan] = "
            f"[bold green]{result.exchange_rate}[/bold green] [bold cyan]{result.target_currency}[/bold cyan]"
        )

        # Copy to clipboard based on format
        if copy_format == CopyFormat.plain:
            clipboard_value = format_plain(result.target_amount)
        elif copy_format == CopyFormat.short:
            clipboard_value = short_formatted
        else:  # default
            clipboard_value = to_formatted

        copy(clipboard_value)
        console.print(f"[green]✓[/green] Copied: [yellow]{clipboard_value}[/yellow]")

    except ParseError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1)
    except Exception:
        console.print_exception()
        raise typer.Exit(code=1)


def main():
    app()


if __name__ == "__main__":
    main()
