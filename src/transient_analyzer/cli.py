import argparse
import json
from pathlib import Path

from transient_analyzer.io.csv_loader import load_trace
from transient_analyzer.models.rc import estimate_tau_632
from transient_analyzer.models.rlc import estimate_rlc_params_from_peaks
from transient_analyzer.report.plot import save_rc_plot, save_rlc_plot
from transient_analyzer.report.report_md import write_rc_report, write_rlc_report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze a transient trace CSV (RC or RLC) and generate outputs."
    )
    parser.add_argument("csv", type=str, help="Path to CSV file containing time,voltage columns")
    parser.add_argument("--out", type=str, default="out", help="Output directory (default: out)")
    parser.add_argument(
        "--mode",
        type=str,
        choices=["rc", "rlc"],
        default="rc",
        help="Analysis mode (default: rc)",
    )

    args = parser.parse_args()

    csv_path = Path(args.csv)
    out_dir = Path(args.out)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    out_dir.mkdir(parents=True, exist_ok=True)

    t, v = load_trace(str(csv_path))

    plot_path = out_dir / "plot.png"
    report_path = out_dir / "report.md"
    metrics_path = out_dir / "metrics.json"

    if args.mode == "rc":
        metrics = estimate_tau_632(t, v)

        save_rc_plot(t, v, metrics, str(plot_path))
        write_rc_report(metrics, str(report_path))

        with open(metrics_path, "w", encoding="utf-8") as f:
            json.dump({"mode": "rc", **metrics}, f, indent=2)

        print(f"[RC] tau ≈ {metrics['tau']:.6f} s")

    else:
        metrics = estimate_rlc_params_from_peaks(t, v)

        # plot peaks + report
        plot_meta = save_rlc_plot(t, v, str(plot_path))
        metrics["num_peaks_plot"] = plot_meta.get("num_peaks", 0.0)

        write_rlc_report(metrics, str(report_path))

        with open(metrics_path, "w", encoding="utf-8") as f:
            json.dump({"mode": "rlc", **metrics}, f, indent=2)

        print("[RLC] Estimated parameters:")
        print(f"  Td    ≈ {metrics['Td_s']:.6f} s")
        print(f"  zeta  ≈ {metrics['zeta']:.4f}")
        print(f"  wd    ≈ {metrics['wd_rad_s']:.2f} rad/s")
        print(f"  w0    ≈ {metrics['w0_rad_s']:.2f} rad/s")
        print(f"  alpha ≈ {metrics['alpha_s_1']:.2f} 1/s")

    print(f"Saved: {plot_path}")
    print(f"Saved: {report_path}")
    print(f"Saved: {metrics_path}")


if __name__ == "__main__":
    main()
