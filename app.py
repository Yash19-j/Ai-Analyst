import streamlit as st
import pandas as pd
import sys
import os

# Add project root to Python path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)

from backend.app.services.analysis_pipeline import AnalysisPipeline
from backend.app.services.report_generator import ReportGenerator

st.set_page_config(page_title="AI Investment Risk Analyzer", layout="wide")

st.title("📊 AI Investment Risk Analyzer")
st.markdown("Upload startup financial data and evaluate investment risk using quantitative modeling.")

# Sidebar inputs
st.sidebar.header("Input Parameters")
founder_equity = st.sidebar.slider("Founder Equity (%)", 0, 100, 60)
simulation_runs = st.sidebar.selectbox("Monte Carlo Simulation Runs", [1000, 3000, 5000, 10000], index=2)

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📂 Uploaded Data")
    st.dataframe(df)

    if st.button("Run Analysis"):
        pipeline = AnalysisPipeline(
            df=df,
            founder_equity=founder_equity,
            simulation_runs=simulation_runs
        )

        results = pipeline.run_full_analysis()

        risk = results["risk_scores"]
        simulation = results["simulation_results"]

        health_score = risk["investment_health_score"] if "investment_health_score" in risk else risk["final_weighted_score"]
        risk_level = risk["risk_level"] if "risk_level" in risk else 100 - health_score
        decision = risk["investment_classification"] if "investment_classification" in risk else risk["investment_decision"]

        st.subheader("📈 Overall Assessment")

        col1, col2, col3 = st.columns(3)

        col1.metric("Investment Health Score", f"{health_score}/100")
        col2.metric("Risk Level", f"{risk_level}/100")
        col3.metric("Investment Classification", decision)

        st.subheader("🎲 Survival Probability")

        st.write(f"12-Month Survival Probability: {simulation['prob_survive_12m']*100:.1f}%")
        st.write(f"24-Month Survival Probability: {simulation['prob_survive_24m']*100:.1f}%")
        st.write(f"Mean Survival Months: {simulation['mean_survival_months']:.2f}")

        report = ReportGenerator(results)
        summary = report.generate_summary()

        st.subheader("🧠 Investor Narrative")
        st.write(summary)

else:
    st.info("Please upload a CSV file to begin analysis.")
