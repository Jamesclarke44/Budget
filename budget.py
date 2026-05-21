import streamlit as st
import json
import os

st.set_page_config(page_title="Budget + Debt Timeline", layout="centered")

st.title("📊 Budget + Debt Timeline + Interest")

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
# CURRENT DEBTS
# =========================
rbc = data["rbc"]
pc = data["pc"]
loc = data["loc"]

# =========================
# INPUTS
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

st.subheader("Debt Payments (Manual)")

savings = st.number_input("Savings", min_value=0, value=100)

rbc_payment = st.number_input("RBC Payment", min_value=0, value=400)
pc_payment = st.number_input("PC Payment", min_value=0, value=100)
loc_payment = st.number_input("LOC Payment", min_value=0, value=100)

# =========================
# INTEREST RATES (IMPORTANT ADDITION)
# =========================
st.subheader("Interest Rates (%)")

rbc_rate = st.number_input("RBC Mastercard Interest %", min_value=0.0, value=19.99)
pc_rate = st.number_input("PC Mastercard Interest %", min_value=0.0, value=19.99)
loc_rate = st.number_input("LOC Interest %", min_value=0.0, value=9.5)

# =========================
# CASH FLOW
# =========================
available = total_income - total_bills
allocated = savings + rbc_payment + pc_payment + loc_payment
remaining = available - allocated

# =========================
# INTEREST CALCULATION (MONTHLY)
# =========================
rbc_interest = rbc * (rbc_rate / 100) / 12
pc_interest = pc * (pc_rate / 100) / 12
loc_interest = loc * (loc_rate / 100) / 12

total_interest = rbc_interest + pc_interest + loc_interest

# =========================
# TIMELINE FUNCTION
# =========================
def months_to_payoff(balance, payment):
    if payment <= 0:
        return float("inf")
    return balance / payment

# =========================
# OUTPUT
# =========================
st.subheader("📊 Financial Summary")

st.write(f"Income: ${total_income}")
st.write(f"Bills: ${total_bills}")
st.write(f"Available After Bills: ${available}")

st.markdown("### 💰 Your Plan")

st.write(f"Savings: ${savings}")
st.write(f"RBC Payment: ${rbc_payment}")
st.write(f"PC Payment: ${pc_payment}")
st.write(f"LOC Payment: ${loc_payment}")

st.metric("Leftover Cash", f"${remaining:.2f}")

# =========================
# INTEREST SECTION
# =========================
st.subheader("💸 Monthly Interest Cost")

st.write(f"RBC Interest: ${rbc_interest:.2f}/month")
st.write(f"PC Interest: ${pc_interest:.2f}/month")
st.write(f"LOC Interest: ${loc_interest:.2f}/month")

st.metric("Total Interest Burn", f"${total_interest:.2f}/month")

# =========================
# DEBT TIMELINE
# =========================
st.subheader("🔮 Debt Payoff Timeline")

rbc_months = months_to_payoff(rbc, rbc_payment)
pc_months = months_to_payoff(pc, pc_payment)
loc_months = months_to_payoff(loc, loc_payment)

st.write(f"RBC Mastercard: ~{rbc_months:.1f} months")
st.write(f"PC Mastercard: ~{pc_months:.1f} months")
st.write(f"Line of Credit: ~{loc_months:.1f} months")

total_debt = rbc + pc + loc
total_payment = rbc_payment + pc_payment + loc_payment

overall = total_debt / max(total_payment, 1)

st.metric("🏁 Full Debt Freedom", f"{overall:.1f} months")

# =========================
# WARNING SYSTEM
# =========================
st.divider()

if remaining < 0:
    st.error("Over budget — you're allocating more than you earn.")
elif remaining < 300:
    st.warning("Tight budget — low buffer.")
else:
    st.success("Budget is stable")

st.caption("Includes interest burn + payoff timeline projection")