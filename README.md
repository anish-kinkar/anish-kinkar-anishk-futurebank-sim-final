# 🔮 FutureBank Sim – AI-Powered Personal Wealth Predictor

This is a **toy personal finance sandbox**.  
You can change your income, expenses, investment returns and a big decision like **buying a car** and see
how your **net worth might evolve** using a **Monte Carlo simulation**.  
Optionally, an **AI advisor** (LLM) explains the scenarios in simple language.

> ⚠️ **Important:** This project is for learning and experimentation only.  
> It is **not** professional financial advice.

---

## 1. Project Structure

```text
FutureBankSim/
├─ app.py                  # Streamlit UI
├─ README.md
├─ requirements.txt
├─ models/
│  ├─ __init__.py
│  └─ config.py            # SimulationConfig dataclass
├─ simulation/
│  ├─ __init__.py
│  └─ monte_carlo.py       # Monte Carlo engine + summaries
└─ advisors/
   ├─ __init__.py
   └─ llm_advisor.py       # Optional LLM-based advice
```

---

## 2. How to Run Locally (very easy steps)

1. **Install Python** (3.9+ is fine).
2. **Download / clone this repo**  
   - If using GitHub:
     ```bash
     git clone https://github.com/your-username/FutureBankSim.git
     cd FutureBankSim
     ```

3. **Create a virtual environment (recommended but optional)**

   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS / Linux:
   source venv/bin/activate
   ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **(Optional) Add your OpenAI API key for AI advice**

   - Create a file called `.env` in the project folder:

     ```text
     OPENAI_API_KEY=sk-your-real-key-here
     ```

   - Or set the environment variable in your terminal:

     ```bash
     export OPENAI_API_KEY=sk-your-real-key-here   # macOS / Linux
     setx OPENAI_API_KEY "sk-your-real-key-here"   # Windows (new terminal after this)
     ```

   If you skip this, the app will still work – you just won’t get LLM-based advice.

6. **Run the app**

   ```bash
   streamlit run app.py
   ```

7. Open the URL shown in the terminal (usually `http://localhost:8501`).

---

## 3. How to Upload to GitHub

1. Create a new repo on GitHub (e.g., `FutureBankSim`).
2. In your local project folder, run:

   ```bash
   git init
   git add .
   git commit -m "Initial commit – FutureBank Sim"
   git branch -M main
   git remote add origin https://github.com/your-username/FutureBankSim.git
   git push -u origin main
   ```

3. Refresh your GitHub page – your code should be there.

---

## 4. How to Deploy (Streamlit Community Cloud – free & easy)

1. Go to Streamlit Community Cloud in your browser.
2. Click **New app** → connect your GitHub account.
3. Select your repo and set:
   - **Main file path**: `app.py`
4. In **Secrets** (on Streamlit Cloud), add your:

   ```text
   OPENAI_API_KEY = "sk-your-real-key-here"
   ```

5. Click **Deploy** – your app will build and you’ll get a shareable URL.

---

## 5. What the Simulator Does (simple words)

- It takes your:
  - Current savings
  - Monthly income and expenses
  - Expected investment return and risk
  - Inflation and income growth
  - Optional car purchase (price, down payment, loan, extra yearly costs)

- It then:
  - Runs **many random futures** (Monte Carlo paths).
  - For each month in the future, your money goes **up or down** depending on:
    - Income – expenses
    - Random investment returns
    - Car loan payments and car costs (if enabled)

- It shows:
  - **Percentile chart** (10%, 50%, 90%) of net worth over time.
  - **Histogram** of final net worth.
  - **Chance of ending negative** (loss probability).
  - Optional **LLM explanation** in simple language.

---

## 6. Good First Project Ideas / Extensions

- Add more scenarios: buying a house, changing jobs, taking a study loan.
- Allow the user to change savings rate over time.
- Export results to CSV.
- Add a “beginner mode” and “advanced mode” with more / fewer inputs.

---

Happy building 🚀  
Again: this is **for learning**, not real financial advice.
