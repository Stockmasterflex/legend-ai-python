import csv
import json
from pathlib import Path

import pandas as pd
import pytest

from app.core.pattern_engine.export import PatternExporter


@pytest.fixture
def sample_patterns():
    return [
        {
            "ticker": "AAPL",
            "pattern": "Cup & Handle",
            "score": 8.4,
            "entry": 175.5,
            "stop": 168.0,
            "target": 190.0,
            "confidence": 0.84,
        },
        {
            "ticker": "MSFT",
            "pattern": "Double Bottom",
            "score": 7.1,
            "entry": 320.5,
            "stop": 305.0,
            "target": 345.0,
            "confidence": 0.71,
        },
    ]


def test_to_csv(tmp_path, sample_patterns):
    exporter = PatternExporter()
    csv_path = exporter.to_csv(sample_patterns, str(tmp_path / "patterns.csv"))
    assert Path(csv_path).exists()

    with open(csv_path, newline="") as handle:
        reader = list(csv.DictReader(handle))
    assert len(reader) == len(sample_patterns)
    assert reader[0]["ticker"] == "AAPL"


def test_to_json(tmp_path, sample_patterns):
    exporter = PatternExporter()
    json_path = exporter.to_json(sample_patterns, str(tmp_path / "patterns.json"))
    data = json.loads(Path(json_path).read_text())
    assert len(data) == 2
    assert data[1]["pattern"] == "Double Bottom"


def test_to_excel(tmp_path, sample_patterns):
    pytest.importorskip("openpyxl")
    exporter = PatternExporter()
    excel_path = exporter.to_excel(sample_patterns, str(tmp_path / "patterns.xlsx"))
    assert Path(excel_path).exists()

    df = pd.read_excel(excel_path)
    assert df.shape[0] == len(sample_patterns)
    assert "pattern" in df.columns


def test_to_clipboard(sample_patterns):
    exporter = PatternExporter()
    text = exporter.to_clipboard(sample_patterns)
    assert "AAPL" in text
    assert "\t" in text  # tab-delimited


def test_batch_export(tmp_path, sample_patterns):
    exporter = PatternExporter()
    scan_results = {"AAPL": [sample_patterns[0]], "MSFT": [sample_patterns[1]]}
    paths = exporter.batch_export(scan_results, str(tmp_path))
    assert len(paths) >= 2  # Excel path is optional if openpyxl is missing
    for path in paths:
        assert Path(path).exists()
