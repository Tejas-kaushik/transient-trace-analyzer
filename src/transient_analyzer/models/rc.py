from typing import Dict, List


def estimate_tau_632(t: List[float], v: List[float]) -> Dict[str, float]:
    """
    Estimate RC time constant tau using the 63.2% method.

    Assumes the trace contains a rising step response.

    Returns a dict with:
      - v0: initial voltage estimate
      - v_inf: final voltage estimate
      - v_tau: 63.2% target voltage
      - t_tau: time when v crosses v_tau
      - tau: time constant (t_tau - t0)
      - t0: start time (assumed t[0])
    """
    if len(t) != len(v) or len(t) < 10:
        raise ValueError("t and v must be same length and have enough points")

    n = len(v)
    k = max(1, n // 10)  # 10% of samples

    v0 = sum(v[:k]) / k
    v_inf = sum(v[-k:]) / k

    v_tau = v0 + 0.632 * (v_inf - v0)

    # Find first crossing of v_tau
    t_tau = None
    for i in range(1, n):
        if v[i - 1] < v_tau <= v[i]:
            # linear interpolation for better accuracy
            dv = v[i] - v[i - 1]
            dt = t[i] - t[i - 1]
            if dv == 0:
                t_tau = t[i]
            else:
                frac = (v_tau - v[i - 1]) / dv
                t_tau = t[i - 1] + frac * dt
            break

    if t_tau is None:
        raise ValueError("Could not find 63.2% crossing in the trace")

    t0 = t[0]
    tau = t_tau - t0

    return {
        "v0": float(v0),
        "v_inf": float(v_inf),
        "v_tau": float(v_tau),
        "t_tau": float(t_tau),
        "t0": float(t0),
        "tau": float(tau),
    }
