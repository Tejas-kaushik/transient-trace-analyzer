from transient_analyzer.io.csv_loader import load_trace
from transient_analyzer.models.rc import estimate_tau_632


def test_tau_estimate_is_reasonable():
    t, v = load_trace("examples/synthetic_rc.csv")
    m = estimate_tau_632(t, v)

    # We expect tau to be positive and within a sensible range for this synthetic trace.
    assert m["tau"] > 0
    assert 0.0001 < m["tau"] < 0.005  # 0.1 ms to 5 ms
