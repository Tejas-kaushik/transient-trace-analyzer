from transient_analyzer.io.csv_loader import load_trace
from transient_analyzer.models.rc import estimate_tau_632
from transient_analyzer.report.plot import save_rc_plot
from transient_analyzer.report.report_md import write_rc_report


def main() -> None:
    t, v = load_trace("examples/synthetic_rc.csv")
    metrics = estimate_tau_632(t, v)

    print("Loaded points:", len(t))
    print(f"V0     ≈ {metrics['v0']:.4f} V")
    print(f"V_inf  ≈ {metrics['v_inf']:.4f} V")
    print(f"V_tau  ≈ {metrics['v_tau']:.4f} V (63.2%)")
    print(f"t_tau  ≈ {metrics['t_tau']:.6f} s")
    print(f"tau    ≈ {metrics['tau']:.6f} s")

    save_rc_plot(t, v, metrics, "plot.png")
    write_rc_report(metrics, "report.md")

    print("Saved plot.png and report.md")


if __name__ == "__main__":
    main()
