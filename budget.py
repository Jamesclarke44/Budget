import streamlit as st
import json
import os

st.set_page_config(page_title="Manual Budget Control", layout="centered")

st.title("📊 Manual Budget & Debt Control")

# =========================
# DATA (DEBT BALANCES)
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

rbc = data["rbc"]
pc = data["pc"]
loc = data["loc"]

# =========================
# INPUTS (ALL MANUAL)
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

st.subheader("Savings & Debt Payments")

savings = st.number_input("Savings Contribution", min_value=0, value=100)

rbc_payment = st.number_input("RBC Mastercard Payment", min_value=0, value=400)
pc_payment = st.number_input("PC Mastercard Payment", min_value=0, value=100)
loc_payment = st.number_input("LOC Payment", min_value=0, value=100)

# =========================
# CALCULATIONS
# =========================
available = total_income - total_bills

total_allocations = savings + rbc_payment + pc_payment + loc_payment

remaining = available - total_allocations

# =========================
# OUTPUT DASHBOARD
# =========================
st.subheader("📊 Summary")

st.write(f"Income: ${total_income}")
st.write(f"Bills: ${total_bills}")
st.write(f"Available After Bills: ${available}")

st.markdown("### 💰 Your Inputs")

st.write(f"Savings: ${savings}")
st.write(f"RBC Payment: ${rbc_payment}")
st.write(f"PC Payment: ${pc_payment}")
st.write(f"LOC Payment: ${loc_payment}")

st.metric("Leftover Cash", f"${remaining:.2f}")

# =========================
# DEBT IMPACT (SIMPLE FORECAST)
# =========================
st.subheader("🔮 Debt Impact (Forecast)")

def months(balance, payment):
    if payment <= 0:
        return float("inf")
    return balance / (payment * 2)  # bi-weekly estimate

st.write("RBC Mastercard:", f"~{months(rbc, rbc_payment):.1f} months")
st.write("PC Mastercard:", f"~{months(pc, pc_payment):.1f} months")
st.write("Line of Credit:", f"~{months(loc, loc_payment):.1f} months")

# =========================
# WARNING SYSTEM
# =========================
st.divider()

if remaining < 0:
    st.error("Over budget — you're allocating more than you have available.")
elif remaining < 300:
    st.warning("Tight budget — low buffer remaining.")
else:
    st.success("Budget is balanced.")

st.caption("Manual control mode: you decide all allocations.")