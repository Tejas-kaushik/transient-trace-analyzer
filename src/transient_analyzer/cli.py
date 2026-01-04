import argparse
import json
from pathlib import Path

from transient_analyzer.io.csv_loader import load_trace
from transient_analyzer.models.rc import estimate_tau_632
from transient_analyzer.report.plot import save_rc_plot
from transient_analyzer.report.report_md import write_rc_report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze a transient trace CSV and estimate RC time constant (tau)."
    )
    parser.add_argument(
        "csv",
        type=str,
        help="Path to CSV file containing time,voltage columns",
    )
    parser.add_argument(
        "--out",
        type=str,
        default="out",
        help="Output directory (default: out)",
    )

    args = parser.parse_args()

    csv_path = Path(args.csv)
    out_dir = Path(args.out)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    out_dir.mkdir(parents=True, exist_ok=True)

    # Load and analyze
    t, v = load_trace(str(csv_path))
    metrics = estimate_tau_632(t, v)

    # Save outputs into out/
    plot_path = out_dir / "plot.png"
    report_path = out_dir / "report.md"
    metrics_path = out_dir / "metrics.json"

    save_rc_plot(t, v, metrics, str(plot_path))
    write_rc_report(metrics, str(report_path))

    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    # Console summary
    print(f"Loaded points: {len(t)}")
    print(f"tau ≈ {metrics['tau']:.6f} s")
    print(f"Saved: {plot_path}")
    print(f"Saved: {report_path}")
    print(f"Saved: {metrics_path}")


if __name__ == "__main__":
    main()
