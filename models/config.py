from dataclasses import dataclass


@dataclass
class SimulationConfig:
    """Configuration for a wealth Monte Carlo simulation.

    All rates are annual decimals (e.g. 0.08 = 8%).
    Monetary values are absolute currency units (₹, $, etc.).
    """

    years: int
    initial_savings: float
    monthly_income: float
    monthly_expenses: float

    income_growth_rate: float  # annual, decimal
    inflation_rate: float      # annual, decimal

    expected_annual_return: float  # annual, decimal
    return_volatility: float       # annual standard deviation, decimal

    # Car-specific settings (used only when with_car=True)
    with_car: bool = False
    car_purchase_year: int = 0
    car_price: float = 0.0
    car_down_payment_pct: float = 0.0  # 0–1
    car_loan_interest_rate: float = 0.0  # annual, decimal
    car_loan_term_years: int = 0
    annual_car_extra_cost: float = 0.0
