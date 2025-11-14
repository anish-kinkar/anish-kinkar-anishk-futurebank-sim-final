# 🔮 FutureBank Sim – AI-Powered Personal Wealth Predictor

### *Visualize your financial future with Monte Carlo simulations + AI advice*

FutureBank Sim is an interactive **personal finance simulator** that predicts your future net worth using **Monte Carlo simulation**, income growth, expenses, inflation, investment returns, and major life decisions like **buying a car**.

It shows:

* 📊 Your future net worth month-by-month
* 🎲 Random market scenarios (good, normal, bad)
* 🚗 Impact of buying a car vs not buying it
* 🤖 Optional AI guidance powered by LLMs
* 🪙 Probability of ending with a loss
* 🔍 Visual percentile ranges (p10, p50, p90)

This tool is designed for students, beginners, and finance enthusiasts who want to understand **how money behaves over time** — in a simple, visual, and fun way.

> ⚠️ *This is a learning tool, not real financial advice.*

---

# ⭐ Why This Project is Unique

Most finance calculators show a **single linear prediction**.
But the future isn’t straight — **markets fluctuate**.

This project uses:

### ✔️ Monte Carlo simulation

to run **1000+ alternate futures**, showing best-case, worst-case, and typical outcomes.

### ✔️ AI-powered personal finance commentary

(optional)
to explain the results in **easy language**
— no technical jargon.

### ✔️ Interactive Web App

built with **Streamlit** so anyone can run it in a browser.

Together, this becomes a **future wealth sandbox** where the user can test “What if?” scenarios, like:

* *“What if I buy a car next year?”*
* *“What if inflation increases?”*
* *“What if my income grows faster?”*
* *“What if I take a loan instead of paying fully?”*

---

# 🧩 Project Description (Easy & Detailed)

FutureBank Sim is a simulation engine that models how your net worth changes over time based on:

## **1️⃣ Your Inputs**

* Current savings
* Monthly income
* Monthly expenses
* Income growth
* Inflation
* Investment return percentage
* Market volatility (risk)

## **2️⃣ Car Purchase Scenario (optional)**

You can simulate the financial impact of buying a car:

* Price of the car
* Down-payment
* Loan term & interest
* Additional yearly expenses
* Purchase year

The model compares:

### **Scenario A → No Car**

Your wealth grows from savings + investment returns.

### **Scenario B → With Car**

Your wealth changes because of:

* Down payment
* Loan EMI
* Maintenance & fuel
* Reduced investment compounding

This helps users visually understand the **long-term hidden cost** of big purchases.

---

# 📈 What Happens Behind the Scenes

## **1. Monte Carlo Simulation**

The app simulates hundreds of alternate possible futures.
Each future month includes:

* Income – expenses
* Random investment return (based on mean + volatility)
* Loan calculations
* Extra car-related costs
* Compounding effects

This produces **1000+ net-worth timelines** → from which we calculate:

* p10 → pessimistic path
* p50 → median/typical path
* p90 → optimistic path
* Probability of going broke
* Final net-worth distribution

## **2. Visualization**

The simulator generates:

### ✔ Percentile net-worth chart

Shows future uncertainty ranges.

### ✔ Final net-worth histogram

Shows how outcomes are distributed.

### ✔ Key financial indicators

* Median final net worth
* Loss probability
* Car impact (in ₹)

## **3. AI Financial Insight (optional)**

If an OpenAI API key is added, the app generates:

* Human-friendly insights
* Simple financial thinking framework
* Pros & cons
* Suggestions like:
  *“Delay the car by 1–2 years to reduce compounding losses.”*

The tone stays **friendly, simple, and clear**.

---

# 🏗 Project Structure

```
FutureBankSim/
│── app.py                     # Main Streamlit UI
│── README.md                  # Project documentation (this file)
│── requirements.txt           # Python dependencies
│
├── models/
│    ├── __init__.py
│    └── config.py             # Dataclass storing all simulation settings
│
├── simulation/
│    ├── __init__.py
│    └── monte_carlo.py        # Monte Carlo engine + net-worth calculations
│
└── advisors/
     ├── __init__.py
     └── llm_advisor.py        # Optional AI-based insight generator
```

### **Folder Purpose Breakdown**

#### 📁 **models/**

Stores input configuration (like car loan settings, inflation, returns).

#### 📁 **simulation/**

All mathematical logic → generates wealth paths.

#### 📁 **advisors/**

AI explanation module — reads the simulation results and generates text.

#### 📁 **root directory**

Streamlit app + configuration files.

---

