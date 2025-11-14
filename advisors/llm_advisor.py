import os
from typing import Dict, Optional

from openai import OpenAI

from models import SimulationConfig


def _format_currency(x: float) -> str:
    return f"₹{x:,.0f}"


def _build_summary_text(
    baseline_cfg: SimulationConfig,
    car_cfg: SimulationConfig,
    baseline_summary: Dict,
    car_summary: Optional[Dict],
    n_sims: int,
) -> str:
    lines = []

    lines.append(
        f"We ran {n_sims} Monte Carlo simulations over {baseline_cfg.years} years for two scenarios:"
    )
    lines.append(
        f"1) Baseline (no car) and 2) Car scenario (buying a car in year {car_cfg.car_purchase_year})"
        if car_cfg.with_car
        else "1) Baseline (no car only – car scenario disabled)."
    )

    lines.append(
        f"In the baseline, the median final net worth was {_format_currency(baseline_summary['final_median'])} "
        f"with a probability of ending negative of {baseline_summary['prob_loss'] * 100:.1f}%."
    )

    if car_cfg.with_car and car_summary is not None:
        delta = car_summary["final_median"] - baseline_summary["final_median"]
        lines.append(
            f"In the car scenario, the median final net worth was {_format_currency(car_summary['final_median'])}, "
            f"which is {_format_currency(delta)} {'higher' if delta > 0 else 'lower' if delta < 0 else 'the same'} "
            f"than the baseline."
        )

    return "\n".join(lines)


def _call_openai(system_prompt: str, user_prompt: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return (
            "AI advisor is disabled because no OpenAI API key was found.\n\n"
            "To enable it, set an environment variable `OPENAI_API_KEY` and restart the app. "
            "For now, interpret the charts as a guide: look at how much risk (spread between p10 and p90) "
            "you are comfortable taking and how strongly the car affects your long-term net worth."
        )

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.4,
        max_tokens=350,
    )

    return response.choices[0].message.content.strip()


def generate_advice(
    baseline_cfg: SimulationConfig,
    car_cfg: SimulationConfig,
    baseline_summary: Dict,
    car_summary: Optional[Dict],
    n_sims: int,
) -> str:
    """Generate natural-language advice based on the simulation results.

    This is **educational only**, not real financial advice.
    """
    summary_text = _build_summary_text(
        baseline_cfg=baseline_cfg,
        car_cfg=car_cfg,
        baseline_summary=baseline_summary,
        car_summary=car_summary,
        n_sims=n_sims,
    )

    system_prompt = (
        "You are a calm, practical personal finance coach. "
        "You never give strict instructions, only pros and cons and questions to reflect on. "
        "You speak in very simple language, assume the user is new to investing, "
        "and you clearly label this as educational only, not real financial advice."
    )

    user_prompt = (
        "Here is a summary of a Monte Carlo wealth simulation comparing scenarios.\n\n"
        f"{summary_text}\n\n"
        "Based on this summary, explain in simple terms how the user can think about: "
        "1) whether buying the car is financially heavy or manageable, "
        "2) how much risk they are taking with their investments, and "
        "3) 2–3 possible next steps they could explore (like changing savings rate or delaying the car). "
        "Keep it under 250 words."
    )

    try:
        return _call_openai(system_prompt, user_prompt)
    except Exception as exc:  # pragma: no cover - defensive
        return (
            "The AI advisor had an error and could not generate custom text right now.\n"
            f"(Technical detail: {exc})\n\n"
            "You can still use the charts above: compare the median outcomes and how wide the p10–p90 band is "
            "to understand the risk and the effect of buying the car."
        )
