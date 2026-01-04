from typing import List


def find_peaks(
    t: List[float],
    v: List[float],
    *,
    min_prominence: float = 0.02,
    min_distance: int = 2,
) -> List[int]:
    """
    Simple local-maximum peak detector.

    Returns indices i where:
      - v[i] is greater than neighbors (local max)
      - peak prominence passes a threshold (relative to surrounding baseline)
      - peaks are separated by at least min_distance samples

    This is intentionally simple (no scipy) for portability.
    """
    if len(t) != len(v) or len(v) < 5:
        return []

    peaks: List[int] = []
    last_i = -10**9

    # Estimate scale to make min_prominence meaningful across traces
    v_min = min(v)
    v_max = max(v)
    scale = max(1e-9, v_max - v_min)
    prom_abs = min_prominence * scale

    for i in range(1, len(v) - 1):
        # local maximum
        if not (v[i] > v[i - 1] and v[i] >= v[i + 1]):
            continue

        # enforce minimum spacing
        if i - last_i < min_distance:
            continue

        # crude prominence: compare to local neighborhood min on each side
        left_min = min(v[max(0, i - 10): i])
        right_min = min(v[i + 1: min(len(v), i + 11)])
        baseline = max(left_min, right_min)
        prominence = v[i] - baseline

        if prominence >= prom_abs:
            peaks.append(i)
            last_i = i

    return peaks
