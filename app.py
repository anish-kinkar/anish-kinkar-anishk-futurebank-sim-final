import os

import numpy as np
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from models.config import SimulationConfig
from simulation.monte_carlo import run_simulation, summarize_paths
from advisors.llm_advisor import generate_advice

load_dotenv()

st.set_page_config(page_title="FutureBank Sim – Personal Wealth Sandbox", layout="wide")

st.title("🔮 FutureBank Sim – AI-Powered Personal Wealth Predictor")
st.write(
    """Play with your future money. Change your income, expenses, investments and
    big decisions (like buying a car) and see how your net worth might evolve over time."""
)

with st.sidebar:
    st.header("📌 Basic Inputs")

    years = st.slider("Simulation horizon (years)", min_value=3, max_value=40, value=15, step=1)
    initial_savings = st.number_input("Current savings (₹)", min_value=0.0, value=200000.0, step=10000.0)
    monthly_income = st.number_input("Monthly income (₹)", min_value=0.0, value=60000.0, step=5000.0)
    monthly_expenses = st.number_input("Monthly expenses (₹)", min_value=0.0, value=40000.0, step=5000.0)

    st.markdown("---")
    st.subheader("📈 Growth & Market Assumptions")

    income_growth_rate_pct = st.number_input(
        "Annual income growth (%)", min_value=0.0, max_value=20.0, value=5.0, step=0.5
    )
    inflation_rate_pct = st.number_input(
        "Annual inflation (%)", min_value=0.0, max_value=15.0, value=5.0, step=0.5
    )
    expected_return_pct = st.number_input(
        "Expected annual investment return (%)", min_value=-10.0, max_value=25.0, value=10.0, step=0.5
    )
    return_volatility_pct = st.number_input(
        "Annual return volatility (risk) (%)", min_value=0.0, max_value=40.0, value=15.0, step=1.0
    )

    st.markdown("---")
    st.subheader("🚗 Car Purchase Scenario (optional)")

    enable_car = st.checkbox("Compare with a car purchase?", value=True)
    car_purchase_year = st.slider("Car purchase in year", min_value=0, max_value=years - 1, value=1)
    car_price = st.number_input("Car price (₹)", min_value=0.0, value=800000.0, step=50000.0)
    car_down_payment_pct = st.slider("Down payment (%)", min_value=0, max_value=100, value=20, step=5)
    car_loan_interest_rate_pct = st.number_input(
        "Car loan interest (annual, %) ", min_value=0.0, max_value=20.0, value=9.0, step=0.5
    )
    car_loan_term_years = st.slider("Car loan term (years)", min_value=1, max_value=10, value=5)
    annual_car_extra_cost = st.number_input(
        "Extra yearly car costs – fuel, insurance, maintenance (₹)", min_value=0.0, value=80000.0, step=10000.0
    )

    st.markdown("---")
    st.subheader("🎲 Simulation Settings")
    n_sims = st.slider("Number of Monte Carlo paths", min_value=200, max_value=3000, value=1000, step=100)
    run_button = st.button("Run simulation")

if not run_button:
    st.info("👈 Set your assumptions in the sidebar and click **Run simulation**.")
    st.stop()

# Build configs
common_kwargs = dict(
    years=years,
    initial_savings=initial_savings,
    monthly_income=monthly_income,
    monthly_expenses=monthly_expenses,
    income_growth_rate=income_growth_rate_pct / 100.0,
    inflation_rate=inflation_rate_pct / 100.0,
    expected_annual_return=expected_return_pct / 100.0,
    return_volatility=return_volatility_pct / 100.0,
)

baseline_cfg = SimulationConfig(with_car=False, **common_kwargs)

car_cfg = SimulationConfig(
    with_car=enable_car,
    car_purchase_year=car_purchase_year,
    car_price=car_price,
    car_down_payment_pct=car_down_payment_pct / 100.0,
    car_loan_interest_rate=car_loan_interest_rate_pct / 100.0,
    car_loan_term_years=car_loan_term_years,
    annual_car_extra_cost=annual_car_extra_cost,
    **common_kwargs,
)

with st.spinner("Running Monte Carlo simulations..."):
    baseline_paths = run_simulation(baseline_cfg, n_sims=n_sims)
    baseline_summary = summarize_paths(baseline_paths)

    if enable_car:
        car_paths = run_simulation(car_cfg, n_sims=n_sims)
        car_summary = summarize_paths(car_paths)
    else:
        car_paths, car_summary = None, None

st.success("Simulation complete ✅")

# === Top metrics ===
col1, col2, col3 = st.columns(3)

col1.metric(
    "Median final net worth – no car",
    f"₹{baseline_summary['final_median']:,.0f}",
)

col2.metric(
    "Chance of losing money – no car",
    f"{baseline_summary['prob_loss'] * 100:.1f}%",
)

if enable_car and car_summary is not None:
    delta_median = car_summary['final_median'] - baseline_summary['final_median']
    col3.metric(
        "Effect of buying the car (median)",
        f"₹{delta_median:,.0f}",
        delta=None,
    )
else:
    col3.metric("Effect of buying the car (median)", "—")

# === Charts ===
st.markdown("## 📊 Net Worth Over Time (Percentile Bands)")

months = baseline_paths.shape[1]
timeline_years = np.arange(months) / 12.0

baseline_df = pd.DataFrame({
    "year": timeline_years,
    "no_car_p10": baseline_summary["p10"],
    "no_car_p50": baseline_summary["p50"],
    "no_car_p90": baseline_summary["p90"],
})

if enable_car and car_summary is not None:
    baseline_df["with_car_p10"] = car_summary["p10"]
    baseline_df["with_car_p50"] = car_summary["p50"]
    baseline_df["with_car_p90"] = car_summary["p90"]

st.line_chart(
    baseline_df.set_index("year"),
    height=400,
)

st.markdown("## 🧪 Distribution of Final Net Worth")

hist_data = {
    "no_car": baseline_summary["final_values"],
}
if enable_car and car_summary is not None:
    hist_data["with_car"] = car_summary["final_values"]

hist_df = pd.DataFrame(
    {k: pd.Series(v) for k, v in hist_data.items()}
)

st.bar_chart(hist_df, height=350)

st.markdown("## 💡 AI Advice – How to Think About This")

advice_text = generate_advice(
    baseline_cfg=baseline_cfg,
    car_cfg=car_cfg,
    baseline_summary=baseline_summary,
    car_summary=car_summary,
    n_sims=n_sims,
)

st.write(advice_text)

st.markdown("---")
st.caption(
    "Educational only – this is a toy simulator, **not** professional financial advice."
)
