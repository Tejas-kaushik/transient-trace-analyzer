from typing import Dict, List
import matplotlib.pyplot as plt


def save_rc_plot(
    t: List[float],
    v: List[float],
    metrics: Dict[str, float],
    out_path: str,
) -> None:
    """
    Save a plot of the RC trace with tau markers.

    Draws:
      - v(t)
      - horizontal line at V_tau
      - vertical line at t_tau
      - marker at (t_tau, V_tau)
    """
    v_tau = metrics["v_tau"]
    t_tau = metrics["t_tau"]

    plt.figure()
    plt.plot(t, v, label="V(t)")
    plt.axhline(v_tau, linestyle="--", label="V_tau (63.2%)")
    plt.axvline(t_tau, linestyle="--", label="t_tau")
    plt.scatter([t_tau], [v_tau], zorder=3)

    plt.title("RC Step Response — Time Constant Estimation")
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()
