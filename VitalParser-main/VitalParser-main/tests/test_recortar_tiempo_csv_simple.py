import csv
from pathlib import Path

from recortar_tiempo_csv import trim_csv_time_range


def make_csv(path: Path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def read_csv_rows(path: Path):
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return list(reader)


def test_trim_simple_inclusive(tmp_path):
    inp = tmp_path / "in.csv"
    out = tmp_path / "out.csv"
    header = ["time", "value"]
    rows = [
        ("2020-01-01 12:00:00", "1"),
        ("2020-01-01 12:01:00", "2"),
        ("2020-01-01 12:06:00", "3"),
    ]
    make_csv(inp, header, rows)

    total, kept = trim_csv_time_range(str(inp), str(out), start="2020-01-01 12:00:00", end="2020-01-01 12:05:00")

    assert total == 3
    assert kept == 2
    out_rows = read_csv_rows(out)
    assert len(out_rows) == 2
    assert out_rows[0]["value"] == "1"


def test_trim_exclusive_and_format(tmp_path):
    inp = tmp_path / "in2.csv"
    out = tmp_path / "out2.csv"
    header = ["Timestamp", "x"]
    rows = [
        ("01/01/2020 12:00:00", "a"),
        ("01/01/2020 12:05:00", "b"),
        ("01/01/2020 12:10:00", "c"),
    ]
    make_csv(inp, header, rows)

    # Provide explicit strptime format and use exclusive bounds
    fmt = "%d/%m/%Y %H:%M:%S"
    total, kept = trim_csv_time_range(str(inp), str(out), start="01/01/2020 12:00:00", end="01/01/2020 12:10:00", timestamp_col="Timestamp", timestamp_format=fmt, inclusive=False)

    assert total == 3
    # exclusive should drop the first and last; keep only middle
    assert kept == 1
    out_rows = read_csv_rows(out)
    assert out_rows[0]["x"] == "b"
