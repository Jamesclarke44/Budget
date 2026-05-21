import streamlit as st
import json
import os

st.set_page_config(page_title="Smart Budget System", layout="centered")

st.title("🧠 Smart Budget & Debt Engine")

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

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

data = load_data()

# =========================
# SESSION STATE
# =========================
if "savings" not in st.session_state:
    st.session_state.savings = data["savings"]

if "rbc" not in st.session_state:
    st.session_state.rbc = data["rbc"]

if "pc" not in st.session_state:
    st.session_state.pc = data["pc"]

if "loc" not in st.session_state:
    st.session_state.loc = data["loc"]

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

# =========================
# DEBT PAYMENTS
# =========================
st.subheader("Debt Payments")

rbc_payment = st.slider("RBC Mastercard", 0, 1000, 400)
pc_payment = st.slider("PC Mastercard", 0, 500, 100)
loc_payment = st.slider("Line of Credit", 0, 500, 100)

# =========================
# SAVINGS
# =========================
buffer = st.number_input("Savings Contribution", value=100)

# =========================
# SMART ENGINE
# =========================
remaining = (
    total_income
    - total_bills
    - buffer
    - rbc_payment
    - pc_payment
    - loc_payment
)

# Auto-adjust if negative
if remaining < 0:
    st.warning("Budget negative. Reduce debt payments or spending.")

# =========================
# PAYDAY BUTTON
# =========================
if st.button("⚡ Run Smart Payday"):

    st.session_state.savings += buffer

    st.session_state.rbc -= rbc_payment
    st.session_state.pc -= pc_payment
    st.session_state.loc -= loc_payment

    # Prevent negative debt
    st.session_state.rbc = max(st.session_state.rbc, 0)
    st.session_state.pc = max(st.session_state.pc, 0)
    st.session_state.loc = max(st.session_state.loc, 0)

    save_data({
        "savings": st.session_state.savings,
        "rbc": st.session_state.rbc,
        "pc": st.session_state.pc,
        "loc": st.session_state.loc
    })

    st.success("Smart payday executed")

# =========================
# DASHBOARD
# =========================
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💰 Income", f"${total_income}")

with col2:
    st.metric("💸 Bills", f"${total_bills}")

with col3:
    st.metric("🔥 Safe to Spend", f"${remaining}")

# =========================
# DEBT TRACKER
# =========================
st.subheader("Debt Tracker")

st.write("### RBC Mastercard")
st.progress(min(st.session_state.rbc / 10000, 1.0))
st.write(f"${st.session_state.rbc}")

st.write("### PC Mastercard")
st.progress(min(st.session_state.pc / 10000, 1.0))
st.write(f"${st.session_state.pc}")

st.write("### Line of Credit")
st.progress(min(st.session_state.loc / 20000, 1.0))
st.write(f"${st.session_state.loc}")

# =========================
# SAVINGS
# =========================
st.subheader("Savings")

st.metric("Emergency Buffer", f"${st.session_state.savings}")

# =========================
# STATUS
# =========================
st.divider()

if remaining < 0:
    st.error("Over budget")
elif remaining < 300:
    st.warning("Tight budget")
else:
    st.success("Budget stable")

st.caption("Priority: RBC Mastercard → PC Mastercard → LOC")