from typing import Dict

import numpy as np

from models import SimulationConfig


def _monthly_from_annual_rate(rate: float) -> float:
    """Convert annual simple rate to approximate monthly rate.

    We keep this simple on purpose for educational clarity.
    """
    return rate / 12.0


def run_simulation(config: SimulationConfig, n_sims: int = 1000) -> np.ndarray:
    """Run Monte Carlo simulation for given config.

    Returns:
        np.ndarray of shape (n_sims, n_months) with the net worth path
        for each simulation.
    """
    months = config.years * 12
    paths = np.zeros((n_sims, months), dtype=float)

    monthly_return_mu = _monthly_from_annual_rate(config.expected_annual_return)
    monthly_return_sigma = config.return_volatility / np.sqrt(12.0)

    monthly_income_growth = _monthly_from_annual_rate(config.income_growth_rate)
    monthly_inflation = _monthly_from_annual_rate(config.inflation_rate)

    purchase_month = config.car_purchase_year * 12 if config.with_car else None

    for i in range(n_sims):
        net_worth = config.initial_savings
        loan_balance = 0.0
        monthly_loan_payment = 0.0

        monthly_income = config.monthly_income
        monthly_expenses = config.monthly_expenses

        for m in range(months):
            # Simple model: income & expenses drift over time
            if m > 0:
                monthly_income *= 1.0 + monthly_income_growth
                monthly_expenses *= 1.0 + monthly_inflation

            net_worth += monthly_income - monthly_expenses

            # --- Car purchase & loan ---
            if config.with_car and purchase_month is not None:
                if m == purchase_month:
                    # Buy the car
                    down_payment = config.car_price * config.car_down_payment_pct
                    loan_balance = max(config.car_price - down_payment, 0.0)
                    net_worth -= down_payment

                    # Compute EMI-style payment
                    if config.car_loan_term_years > 0 and loan_balance > 0:
                        r = _monthly_from_annual_rate(config.car_loan_interest_rate)
                        n = config.car_loan_term_years * 12
                        if r > 0:
                            monthly_loan_payment = loan_balance * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
                        else:
                            monthly_loan_payment = loan_balance / n

                # Loan repayments
                if purchase_month is not None and m >= purchase_month and loan_balance > 0 and monthly_loan_payment > 0:
                    r = _monthly_from_annual_rate(config.car_loan_interest_rate)
                    interest = loan_balance * r
                    principal = monthly_loan_payment - interest
                    loan_balance = max(loan_balance - principal, 0.0)
                    net_worth -= monthly_loan_payment

                # Extra yearly car costs (fuel, insurance, maintenance)
                if purchase_month is not None and m >= purchase_month and (m - purchase_month) % 12 == 0:
                    net_worth -= config.annual_car_extra_cost

            # --- Investment returns ---
            shock = np.random.normal(monthly_return_mu, monthly_return_sigma)
            net_worth *= 1.0 + shock

            paths[i, m] = net_worth

    return paths


def summarize_paths(paths: np.ndarray) -> Dict[str, np.ndarray]:
    """Return useful summary statistics from simulation paths."""
    if paths.ndim != 2:
        raise ValueError("paths must have shape (n_sims, n_months)")

    final_values = paths[:, -1]
    p10 = np.percentile(paths, 10, axis=0)
    p50 = np.percentile(paths, 50, axis=0)
    p90 = np.percentile(paths, 90, axis=0)

    prob_loss = float(np.mean(final_values < 0.0))

    return {
        "p10": p10,
        "p50": p50,
        "p90": p90,
        "final_values": final_values,
        "final_median": float(np.median(final_values)),
        "final_mean": float(np.mean(final_values)),
        "prob_loss": prob_loss,
    }
