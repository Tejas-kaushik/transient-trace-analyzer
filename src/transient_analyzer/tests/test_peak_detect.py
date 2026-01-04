from transient_analyzer.io.csv_loader import load_trace
from transient_analyzer.signals.detect import find_peaks


def test_find_peaks_finds_some_peaks_on_synthetic_rlc():
    t, v = load_trace("examples/synthetic_rlc.csv")
    peaks = find_peaks(t, v, min_prominence=0.05, min_distance=2)

    # We expect multiple peaks in a ringing waveform
    assert len(peaks) >= 2

    # Peaks should be valid indices
    assert all(0 < i < len(v) - 1 for i in peaks)

    # Each returned index should actually be a local maximum
    for i in peaks:
        assert v[i] > v[i - 1]
        assert v[i] >= v[i + 1]
