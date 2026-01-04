import csv
from typing import List, Tuple


def load_trace(path: str) -> Tuple[List[float], List[float]]:
    """
    Load a CSV file containing two numeric columns: time, voltage.

    - Skips header/non-numeric rows automatically.
    - Returns two lists: t (seconds), v (volts).

    Expected format (example):
        t,v
        0.0000,0.12
        0.0001,0.15
        ...
    """
    t: List[float] = []
    v: List[float] = []

    with open(path, "r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 2:
                continue

            try:
                ti = float(row[0].strip())
                vi = float(row[1].strip())
            except ValueError:
                # header or non-numeric row -> skip
                continue

            t.append(ti)
            v.append(vi)

    if len(t) < 5:
        raise ValueError(f"Not enough numeric rows found in CSV: {path}")

    return t, v
