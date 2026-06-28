"""
Local input layer for the stock watchlist.

This service reads symbols from a plain-text file and provides them to the
analysis pipeline. In the high-level design, this is the configuration/input
layer that feeds the engine.
"""

from pathlib import Path


class WatchlistService:
    def __init__(self, file_path=None):
        if file_path is None:
            file_path = Path(__file__).resolve().parents[1] / "data" / "watchlist.txt"
        self.file_path = Path(file_path)

        if not self.file_path.is_absolute():
            self.file_path = (Path(__file__).resolve().parents[1] / self.file_path).resolve()

    def get_symbols(self):
        """Read and return the non-empty symbols listed in the watchlist file."""
        symbols = []
        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                for line in file:
                    symbol = line.strip()
                    if symbol:
                        symbols.append(symbol)
        except FileNotFoundError:
            print(f"[WatchlistService] File not found: {self.file_path}")

        return symbols