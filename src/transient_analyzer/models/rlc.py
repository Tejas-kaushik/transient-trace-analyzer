import math
from typing import Dict, List

from transient_analyzer.signals.detect import find_peaks


def estimate_rlc_params_from_peaks(t: List[float], v: List[float]) -> Dict[str, float]:
    """
    Estimate RLC underdamped parameters from successive peak times/amplitudes.

    Uses:
      - Td = average time between peaks
      - log decrement: delta = ln(A1/A2)
      - zeta = delta / sqrt((2*pi)^2 + delta^2)
      - wd = 2*pi / Td
      - w0 = wd / sqrt(1 - zeta^2)
      - alpha = zeta * w0

    Assumes v contains a decaying oscillation with at least 2 peaks.
    """
    peaks = find_peaks(t, v, min_prominence=0.05, min_distance=2)
    if len(peaks) < 2:
        raise ValueError("Not enough peaks detected for RLC estimation")

    # Use first two peaks for simplest MVP (can improve to average later)
    i1, i2 = peaks[0], peaks[1]
    t1, t2 = t[i1], t[i2]
    A1, A2 = abs(v[i1]), abs(v[i2])

    if t2 <= t1:
        raise ValueError("Peak times not increasing")
    Td = t2 - t1

    if A1 <= 0 or A2 <= 0:
        raise ValueError("Peak amplitudes must be positive")

    delta = math.log(A1 / A2)

    # zeta from log decrement relationship (standard underdamped second-order system)
    zeta = delta / math.sqrt((2 * math.pi) ** 2 + delta**2)

    wd = 2 * math.pi / Td

    # guard against numerical issues
    if zeta >= 1.0:
        raise ValueError("Estimated zeta >= 1 (not underdamped or peaks incorrect)")

    w0 = wd / math.sqrt(1.0 - zeta**2)
    alpha = zeta * w0

    return {
        "Td_s": float(Td),
        "delta": float(delta),
        "zeta": float(zeta),
        "wd_rad_s": float(wd),
        "w0_rad_s": float(w0),
        "alpha_s_1": float(alpha),
        "peak1_time_s": float(t1),
        "peak2_time_s": float(t2),
        "peak1_amp": float(A1),
        "peak2_amp": float(A2),
        "num_peaks": float(len(peaks)),
    }
