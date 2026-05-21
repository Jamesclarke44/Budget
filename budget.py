import streamlit as st
import json
import os
import matplotlib.pyplot as plt

st.set_page_config(page_title="Budget + Debt Graph", layout="centered")

st.title("📊 Budget + Debt Timeline + Graph")

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
# DEBTS
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

st.subheader("Debt Payments")

rbc_payment = st.number_input("RBC Payment", min_value=0, value=400)
pc_payment = st.number_input("PC Payment", min_value=0, value=100)
loc_payment = st.number_input("LOC Payment", min_value=0, value=100)

# =========================
# CASH FLOW
# =========================
available = total_income - total_bills

allocated = rbc_payment + pc_payment + loc_payment
remaining = available - allocated

# =========================
# SIMULATION ENGINE (GRAPH)
# =========================
st.subheader("📉 Debt Payoff Graph (Projection)")

months = 60  # simulate 5 years

def simulate_debt(balance, payment):
    values = []
    current = balance
    for _ in range(months):
        current -= payment
        if current < 0:
            current = 0
        values.append(current)
    return values

rbc_curve = simulate_debt(rbc, rbc_payment)
pc_curve = simulate_debt(pc, pc_payment)
loc_curve = simulate_debt(loc, loc_payment)

fig, ax = plt.subplots()

ax.plot(rbc_curve, label="RBC Mastercard")
ax.plot(pc_curve, label="PC Mastercard")
ax.plot(loc_curve, label="Line of Credit")

ax.set_title("Debt Payoff Projection")
ax.set_xlabel("Months")
ax.set_ylabel("Remaining Balance ($)")
ax.legend()

st.pyplot(fig)

# =========================
# SUMMARY
# =========================
st.subheader("📊 Summary")

st.write(f"Income: ${total_income}")
st.write(f"Bills: ${total_bills}")
st.write(f"Available After Bills: ${available}")

st.write(f"RBC Payment: ${rbc_payment}")
st.write(f"PC Payment: ${pc_payment}")
st.write(f"LOC Payment: ${loc_payment}")

st.metric("Leftover Cash", f"${remaining:.2f}")

# =========================
# WARNING SYSTEM
# =========================
st.divider()

if remaining < 0:
    st.error("Over budget")
elif remaining < 300:
    st.warning("Tight budget")
else:
    st.success("Stable cash flow")

st.caption("Graph shows linear payoff projection based on your inputs")