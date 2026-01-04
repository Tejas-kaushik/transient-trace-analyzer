from transient_analyzer.io.csv_loader import load_trace
from transient_analyzer.models.rlc import estimate_rlc_params_from_peaks


def test_estimate_rlc_params_returns_valid_values():
    t, v = load_trace("examples/synthetic_rlc.csv")
    m = estimate_rlc_params_from_peaks(t, v)

    assert m["Td_s"] > 0
    assert 0 <= m["zeta"] < 1
    assert m["wd_rad_s"] > 0
    assert m["w0_rad_s"] > 0
    assert m["alpha_s_1"] >= 0
