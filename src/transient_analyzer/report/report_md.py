from typing import Dict


def write_rc_report(metrics: Dict[str, float], out_path: str) -> None:
    """
    Write a simple markdown report for RC tau estimation.
    """
    lines = [
        "# RC Step Response Report",
        "",
        "## Estimated Parameters",
        f"- V0: **{metrics['v0']:.4f} V**",
        f"- V∞: **{metrics['v_inf']:.4f} V**",
        f"- Vτ (63.2%): **{metrics['v_tau']:.4f} V**",
        f"- tτ: **{metrics['t_tau']:.6f} s**",
        f"- τ: **{metrics['tau']:.6f} s**",
        "",
        "## Notes",
        "- τ estimated using the 63.2% crossing method on a rising step response.",
    ]

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def write_rlc_report(metrics: Dict[str, float], out_path: str) -> None:
    """
    Write a simple markdown report for RLC underdamped parameter estimation.
    """
    lines = [
        "# RLC Ringing Report",
        "",
        "## Estimated Parameters",
        f"- Td (peak-to-peak period): **{metrics['Td_s']:.6f} s**",
        f"- Log decrement δ: **{metrics['delta']:.4f}**",
        f"- Damping ratio ζ: **{metrics['zeta']:.4f}**",
        f"- ωd (damped): **{metrics['wd_rad_s']:.2f} rad/s**",
        f"- ω0 (natural): **{metrics['w0_rad_s']:.2f} rad/s**",
        f"- α (decay rate): **{metrics['alpha_s_1']:.2f} 1/s**",
        "",
        "## Peak Info",
        f"- Peaks detected: **{int(metrics.get('num_peaks', 0))}**",
        f"- Peak1 time: **{metrics['peak1_time_s']:.6f} s**, amp: **{metrics['peak1_amp']:.4f}**",
        f"- Peak2 time: **{metrics['peak2_time_s']:.6f} s**, amp: **{metrics['peak2_amp']:.4f}**",
        "",
        "## Notes",
        "- Parameters estimated from the first two detected peaks.",
        "- Assumes an underdamped second-order response.",
    ]

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
