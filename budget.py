import streamlit as st
import json
import os

st.set_page_config(page_title="Budget Dashboard", layout="centered")

st.title("📊 Budget & Debt Dashboard")

# =========================
# LOAD / SAVE
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
# INPUTS
# =========================
st.subheader("Income")

income = st.number_input("Paycheque", value=5296)
extra = st.number_input("Overtime", value=0)

total_income = income + extra

# =========================
# BILLS
# =========================
st.subheader("Bills")

mortgage = st.number_input("Mortgage", value=3260)
insurance = st.number_input("Insurance", value=650)
telus = st.number_input("Telus", value=150)
enmax = st.number_input("ENMAX", value=250)
fuel = st.number_input("Fuel", value=200)
food = st.number_input("Food", value=400)

total_bills = mortgage + insurance + telus + enmax + fuel + food

# =========================
# ACTIONS
# =========================
st.subheader("Payday Plan")

buffer = st.number_input("Savings Contribution", value=100)
rbc_payment = st.number_input("RBC Payment", value=400)

remaining = total_income - total_bills - buffer - rbc_payment

if st.button("💰 Run Payday"):

    st.session_state.savings += buffer
    st.session_state.rbc -= rbc_payment

    if st.session_state.rbc < 0:
        st.session_state.rbc = 0

    save_data({
        "savings": st.session_state.savings,
        "rbc": st.session_state.rbc,
        "pc": st.session_state.pc,
        "loc": st.session_state.loc
    })

    st.success("Payday processed!")

# =========================
# VISUAL DASHBOARD
# =========================

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💰 Income", f"${total_income}")

with col2:
    st.metric("💸 Bills", f"${total_bills}")

with col3:
    st.metric("🔥 Safe to Spend", f"${remaining}")

st.divider()

# =========================
# DEBT VISUALS
# =========================
st.subheader("Debt Tracker")

st.write("### RBC Mastercard")
st.progress(st.session_state.rbc / 10000)
st.write(f"Balance: ${st.session_state.rbc}")

st.write("### PC Mastercard")
st.progress(st.session_state.pc / 10000)
st.write(f"Balance: ${st.session_state.pc}")

st.write("### Line of Credit")
st.progress(st.session_state.loc / 20000)
st.write(f"Balance: ${st.session_state.loc}")

# =========================
# SAVINGS
# =========================
st.subheader("Savings Buffer")
st.metric("Saved", f"${st.session_state.savings}")

# =========================
# WARNING SYSTEM
# =========================
st.divider()

if remaining < 0:
    st.error("Over budget — adjust spending or payments.")
elif remaining < 300:
    st.warning("Tight budget — be careful.")
else:
    st.success("Budget stable")

st.caption("Priority: RBC Mastercard → PC Mastercard → Line of Credit")