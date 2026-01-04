# Transient Trace Analyzer (RC/RLC)

A Python tool that analyzes oscilloscope-style time/voltage traces to estimate transient parameters and generate a plot + report.

✅ Current MVP: **RC step response → time constant τ (63.2% method)**  
🚧 Next: **RLC underdamped response → α, ωd, ω0, ζ**

---

## What it does (RC MVP)
Given a CSV trace containing `(time, voltage)`:
- estimates **V0**, **V∞**
- computes **Vτ = V0 + 0.632(V∞ − V0)**
- finds **tτ** and calculates **τ**
- saves:
  - `plot.png` (trace with τ markers)
  - `report.md` (summary report)

---

## Quickstart

### 1) Install dependencies
```bash
pip install -r requirements.txt

## Example plot
![RC plot](images/plot.png)
