import streamlit as st
import json
import os

st.set_page_config(page_title="Smart Auto Budget", layout="centered")

st.title("🧠 Auto Budget & Debt Engine")

# =========================
# DATA STORAGE
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
# INPUTS (MANUAL ONLY)
# =========================
st.subheader("Income")

income = st.number_input("Income", min_value=0, value=5296)
overtime = st.number_input("Overtime", min_value=0, value=0)

total_income = income + overtime

st.subheader("Bills")

mortgage = st.number_input("Mortgage", min_value=0, value=3018)
insurance = st.number_input("Insurance", min_value=0, value=574)
telus = st.number_input("Telus", min_value=0, value=150)
enmax = st.number_input("ENMAX", min_value=0, value=250)
fuel = st.number_input("Fuel", min_value=0, value=200)
food = st.number_input("Food", min_value=0, value=400)

total_bills = (
    mortgage +
    insurance +
    telus +
    enmax +
    fuel +
    food
)

# =========================
# DEBT BALANCES
# =========================
rbc = data["rbc"]
pc = data["pc"]
loc = data["loc"]

st.subheader("Debt Balances")

st.write(f"RBC Mastercard: ${rbc}")
st.write(f"PC Mastercard: ${pc}")
st.write(f"Line of Credit: ${loc}")

# =========================
# CORE CALCULATION ENGINE
# =========================
available = total_income - total_bills

# -------------------------
# RULES (AUTO ALLOCATION)
# -------------------------

# 1. Emergency buffer rule
savings_target = 100

# 2. Remaining after savings
after_savings = available - savings_target

if after_savings < 0:
    savings_target = max(0, available * 0.1)
    after_savings = available - savings_target

# 3. Debt priority weights
# RBC = highest priority
rbc_weight = 0.6
pc_weight = 0.3
loc_weight = 0.1

rbc_payment = after_savings * rbc_weight
pc_payment = after_savings * pc_weight
loc_payment = after_savings * loc_weight

# =========================
# RECOMMENDED PLAN OUTPUT
# =========================
st.subheader("📊 Recommended Auto Plan")

st.write(f"Income: ${total_income}")
st.write(f"Bills: ${total_bills}")
st.write(f"Available After Bills: ${available}")

st.markdown("### 💰 Auto Allocation")

st.write(f"✔ Savings: ${savings_target:.2f}")
st.write(f"🔥 RBC Payment: ${rbc_payment:.2f}")
st.write(f"💳 PC Payment: ${pc_payment:.2f}")
st.write(f"🏦 LOC Payment: ${loc_payment:.2f}")

remaining = available - (savings_target + rbc_payment + pc_payment + loc_payment)

st.metric("Leftover Cash", f"${remaining:.2f}")

# =========================
# DEBT PROJECTION (SIMPLE)
# =========================
st.subheader("🔮 Payoff Estimate")

def months(balance, payment):
    if payment <= 0:
        return float("inf")
    return balance / (payment * 2)  # bi-weekly assumption

st.write(f"RBC: ~{months(rbc, rbc_payment):.1f} months")
st.write(f"PC: ~{months(pc, pc_payment):.1f} months")
st.write(f"LOC: ~{months(loc, loc_payment):.1f} months")

# =========================
# WARNING SYSTEM
# =========================
st.divider()

if remaining < 0:
    st.error("Over-allocated budget — reduce spending or debt targets")
elif remaining < 300:
    st.warning("Tight budget")
else:
    st.success("Healthy cash flow")