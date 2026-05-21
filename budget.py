import streamlit as st
import json
import os

st.set_page_config(page_title="Predictive Budget System", layout="centered")

st.title("🔮 Predictive Budget & Debt System")

# =========================
# LOAD DATA
# =========================
DATA_FILE = "budget_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)

    return {
        "savings": 0,
        "rbc": 7882,
        "pc": 5119,
        "loc": 15463
    }

data = load_data()

# =========================
# INCOME
# =========================
st.subheader("Income")

income = st.number_input("Monthly Income", value=5296)
overtime = st.number_input("Overtime", value=0)

total_income = income + overtime

# =========================
# BILLS
# =========================
st.subheader("Bills")

mortgage = st.number_input("Mortgage", value=3018)
insurance = st.number_input("Insurance", value=574)
telus = st.number_input("Telus", value=150)
enmax = st.number_input("ENMAX", value=250)
fuel = st.number_input("Fuel", value=200)
food = st.number_input("Food", value=400)

total_bills = (
    mortgage +
    insurance +
    telus +
    enmax +
    fuel +
    food
)

available = total_income - total_bills

# =========================
# PAYMENT STRATEGY
# =========================
st.subheader("Debt Strategy")

rbc_payment = st.slider("RBC Payment", 0, 1000, 400)
pc_payment = st.slider("PC Payment", 0, 500, 100)
loc_payment = st.slider("LOC Payment", 0, 500, 100)

# =========================
# CURRENT DEBT
# =========================
rbc = data["rbc"]
pc = data["pc"]
loc = data["loc"]

# =========================
# FORECAST ENGINE
# =========================
st.subheader("🔮 Debt Forecast")

def payoff_months(balance, payment):
    if payment <= 0:
        return float("inf")
    return balance / payment

rbc_months = payoff_months(rbc, rbc_payment)
pc_months = payoff_months(pc, pc_payment)
loc_months = payoff_months(loc, loc_payment)

st.write(f"RBC Mastercard: ~{rbc_months:.1f} months")
st.write(f"PC Mastercard: ~{pc_months:.1f} months")
st.write(f"Line of Credit: ~{loc_months:.1f} months")

# =========================
# OVERALL TIMELINE
# =========================
total_debt = rbc + pc + loc
total_payment = rbc_payment + pc_payment + loc_payment

overall_months = total_debt / max(total_payment, 1)

st.metric("🏁 Estimated Debt-Free Timeline", f"{overall_months:.1f} months")

# =========================
# WHAT-IF SIMULATOR
# =========================
st.subheader("⚡ What-If Simulator")

extra_payment = st.slider("Extra Monthly Payment", 0, 1000, 200)

faster_months = total_debt / max(total_payment + extra_payment, 1)

st.success(f"With extra payments: ~{faster_months:.1f} months")

# =========================
# CASH FLOW
# =========================
st.divider()

remaining = (
    total_income
    - total_bills
    - rbc_payment
    - pc_payment
    - loc_payment
)

st.metric("💰 Available After Payments", f"${remaining}")

if remaining < 0:
    st.error("Over budget")
elif remaining < 300:
    st.warning("Tight month")
else:
    st.success("Stable cash flow")