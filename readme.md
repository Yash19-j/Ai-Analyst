# 📊 AI Analyst

> Quantitative startup investment risk analysis — runway forecasting, Monte Carlo survival modeling, and a weighted multi-factor health score, all from a single CSV upload.

Upload a startup's monthly financials. Get back a runway forecast, 12 / 18 / 24-month survival probabilities, a 0–100 investment health score, and a written investor narrative with an `INVEST` / `CAUTION` / `AVOID` verdict.

---

## 🌐 Live Demo

> **Demo link:** _will be added here once deployed._

---

## 🚀 Features

- **Deterministic financial engine** — average burn, runway in months, revenue CAGR, growth volatility.

- **Stability analytics** — revenue/expense growth means and volatility, with **shrinkage adjustment** for small datasets so 3-month histories don't get artificially penalized.

- **Capital efficiency metrics** — burn multiple, revenue-to-expense ratio, capital efficiency ratio.

- **Monte Carlo runway simulation** — 5,000+ iterations using log-normal revenue growth and normal expense growth; outputs 12 / 18 / 24-month survival probabilities and mean survival horizon.

- **Weighted risk scoring engine** — combines four sub-scores into a final 0–100 health score with an `INVEST` / `CAUTION` / `AVOID` classification:
  - Financial Health — **30%**
  - Growth Stability — **30%**
  - Capital Efficiency — **25%**
  - Governance (founder equity) — **15%**

- **Investor narrative generator** — converts the numerical output into a structured, human-readable summary suitable for a memo or deck.

- **Streamlit UI** with sliders for founder equity and simulation runs, plus a CLI runner (`test_run.py`) for batch testing.

---

## 🏗️ Architecture

```
            ┌────────────────────┐
   CSV ──►  │  AnalysisPipeline  │  ◄── founder_equity, simulation_runs
            └─────────┬──────────┘
                      │
   ┌──────────────────┼──────────────────┬──────────────────┐
   ▼                  ▼                  ▼                  ▼
FinancialEngine  StabilityMetrics  EfficiencyMetrics  MonteCarloSimulation
   │                  │                  │                  │
   └──────────────────┴────────┬─────────┴──────────────────┘
                               ▼
                      RiskScoringEngine
                               │
                               ▼
                       ReportGenerator
                               │
                               ▼
                    Streamlit UI / CLI output
```

Each service is a single-responsibility class with input validation, so individual stages can be tested, swapped, or reused independently.

---

## 🧰 Tech Stack

- **Python 3.9+**
- **Streamlit** — interactive UI
- **pandas** — data ingestion and transformation
- **NumPy** — vectorized math and Monte Carlo sampling

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/Yash19-j/Ai-Analyst.git
cd Ai-Analyst

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate          # macOS / Linux
# venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Usage

### Option 1 — Streamlit web app

```bash
streamlit run app.py
```

Then open the URL Streamlit prints (typically `http://localhost:8501`), set the founder equity slider and simulation runs, upload a CSV, and click **Run Analysis**.

### Option 2 — Command-line test runner

```bash
python test_run.py
```

This loads `sample_data/failing_startup.csv` by default and prints the full analysis plus the investor narrative. Edit the `csv_path` line in `test_run.py` to point at any other file.

### Input CSV format

Your CSV must contain these columns (at least 2 rows, ideally 6+):

| Month | Revenue | Expenses | Cash    |
|-------|---------|----------|---------|
| 1     | 50000   | 80000    | 500000  |
| 2     | 60000   | 85000    | 470000  |
| ...   | ...     | ...      | ...     |

Two sample files are included in `sample_data/`:

- `demo_startup.csv` — a healthy, growing company.
- `failing_startup.csv` — accelerating burn, deteriorating economics.

---

## 📐 Methodology Notes

**Volatility shrinkage.** When the dataset has fewer than 6 points, raw standard deviation is unreliable. `StabilityMetrics` applies a multiplier (0.85 for 3–5 points, 0.7 for fewer) to dampen inflated volatility before it feeds the simulation. Data confidence is reported as `HIGH` / `MEDIUM` / `LOW` alongside every run.

**Monte Carlo dynamics.**
- Revenue: log-normal with drift correction — `R_{t+1} = R_t · exp(μ − 0.5σ² + σZ)`.
- Expenses: simple normal multiplicative growth — `E_{t+1} = E_t · (1 + g)`.
- A run ends when cash crosses zero or hits the 60-month horizon.

**Scoring bands.**

| Final Score | Classification |
|-------------|----------------|
| ≥ 75        | INVEST         |
| 50 – 74     | CAUTION        |
| < 50        | AVOID          |

---

## 📁 Project Structure

```
.
├── app.py                          # Streamlit frontend
├── test_run.py                     # CLI runner
├── requirements.txt                # Python dependencies
├── sample_data/
│   ├── demo_startup.csv
│   └── failing_startup.csv
└── backend/
    └── app/
        └── services/
            ├── financial_engine.py     # Burn, runway, CAGR, volatility
            ├── stability_metrics.py    # Growth stability + shrinkage
            ├── efficiency_metrics.py   # Burn multiple, ratios
            ├── simulation.py           # Monte Carlo runway
            ├── risk_scoring.py         # Weighted scoring + classification
            ├── analysis_pipeline.py    # Orchestrator
            └── report_generator.py     # Investor narrative
```

---

## 🛣️ Roadmap

- LLM-generated qualitative summaries (currently rule-based).
- Sector benchmarking — compare against SaaS / D2C / fintech medians.
- PDF export of the full investor memo.
- Scenario stress testing (e.g., revenue down 30%, expense up 20%).
- Persistent storage for past analyses and side-by-side comparisons.
- Public deployment on Streamlit Cloud / Hugging Face Spaces.

---

## 📝 Project Status

This is a **learning project** built to explore quantitative finance modeling, Monte Carlo methods, and end-to-end Python application design. Feedback and suggestions are welcome.

---

## 👤 Author

**Yash Jindal**

- LinkedIn: [linkedin.com/in/yashjindal19](https://www.linkedin.com/in/yashjindal19/)
- Email: [jindal198yjbj@gmail.com](mailto:jindal198yjbj@gmail.com)
- GitHub: [@Yash19-j](https://github.com/Yash19-j)

---

## 📄 License

**Copyright © 2026 Yash Jindal. All Rights Reserved.**

AI Analyst is the proprietary work of Yash Jindal. No part of this codebase may be copied, modified, distributed, sublicensed, or used in any form — commercial or non-commercial — without prior written permission from the copyright holder.

For licensing inquiries, contact: **jindal198yjbj@gmail.com**