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
