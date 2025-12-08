from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

DEFAULT_FIELDS = ["ticker", "pattern", "score", "entry", "stop", "target", "confidence"]


class PatternExporter:
    """Utility class for exporting pattern results into multiple formats."""

    def __init__(self) -> None:
        self.default_fields = list(DEFAULT_FIELDS)

    def to_csv(self, patterns: List[Dict[str, Any]], filename: str) -> str:
        """Export patterns to CSV."""
        path = self._prepare_path(filename)
        rows = [self._normalize_row(pat) for pat in patterns]

        with path.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=self.default_fields)
            writer.writeheader()
            writer.writerows(rows)

        return str(path)

    def to_json(self, patterns: List[Dict[str, Any]], filename: str) -> str:
        """Export patterns to JSON (includes full metadata)."""
        path = self._prepare_path(filename)
        with path.open("w") as handle:
            json.dump(patterns, handle, indent=2, default=str)
        return str(path)

    def to_excel(self, patterns: List[Dict[str, Any]], filename: str) -> str:
        """Export patterns to Excel with header formatting."""
        try:
            import openpyxl  # noqa: F401
        except ImportError as exc:  # pragma: no cover - depends on optional dependency
            raise ImportError("openpyxl is required for Excel export") from exc

        path = self._prepare_path(filename)
        df = self._to_dataframe(patterns)

        with pd.ExcelWriter(path, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Patterns")
            try:
                from openpyxl.styles import Font

                worksheet = writer.sheets["Patterns"]
                for cell in next(worksheet.iter_rows(min_row=1, max_row=1)):
                    cell.font = Font(bold=True)
            except Exception:
                # Formatting is best-effort; still return a valid workbook
                pass

        return str(path)

    def to_clipboard(self, patterns: List[Dict[str, Any]]) -> str:
        """
        Copy patterns to clipboard as tab-delimited text.

        Returns the tab-delimited string regardless of clipboard availability.
        """
        df = self._to_dataframe(patterns)
        tab_text = df.to_csv(sep="\t", index=False)

        try:
            pd.io.clipboard.copy(tab_text)
        except Exception:
            # Clipboard might be unavailable in CI; returning the text is enough.
            pass

        return tab_text

    def batch_export(
        self, scan_results: Dict[str, List[Any]], output_dir: str
    ) -> List[str]:
        """Export aggregated scan results (multiple tickers) to CSV, JSON, and Excel."""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        base = Path(output_dir)
        base.mkdir(parents=True, exist_ok=True)

        flattened: List[Dict[str, Any]] = []
        for ticker, patterns in (scan_results or {}).items():
            for pat in patterns or []:
                record = dict(pat)
                record.setdefault("ticker", ticker)
                flattened.append(record)

        paths = [
            self.to_csv(flattened, str(base / f"patterns_{timestamp}.csv")),
            self.to_json(flattened, str(base / f"patterns_{timestamp}.json")),
        ]

        try:
            paths.append(
                self.to_excel(flattened, str(base / f"patterns_{timestamp}.xlsx"))
            )
        except ImportError:
            # Excel export is optional when openpyxl is unavailable.
            pass
        return paths

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #
    def _prepare_path(self, filename: str) -> Path:
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def _normalize_row(self, pattern: Dict[str, Any]) -> Dict[str, Any]:
        """Coerce a pattern dict into the CSV schema."""
        ticker = pattern.get("ticker") or pattern.get("symbol")
        return {
            "ticker": ticker,
            "pattern": pattern.get("pattern") or pattern.get("pattern_type"),
            "score": pattern.get("score"),
            "entry": pattern.get("entry"),
            "stop": pattern.get("stop"),
            "target": pattern.get("target"),
            "confidence": pattern.get("confidence"),
        }

    def _to_dataframe(self, patterns: List[Dict[str, Any]]) -> pd.DataFrame:
        if not patterns:
            return pd.DataFrame(columns=self.default_fields)

        rows = [self._normalize_row(pat) for pat in patterns]
        df = pd.DataFrame(rows, columns=self.default_fields)
        return df
