import streamlit as st

st.title("Simple Budget & Debt Tracker")

# -------------------------
# INPUTS
# -------------------------
income = st.number_input("Paycheque Income", value=2600)

st.subheader("Optional Adjustments")
extra_income = st.number_input("Overtime / Extra Income", value=0)

total_income = income + extra_income

# -------------------------
# FIXED MONTHLY BILLS
# -------------------------
mortgage = 3260
insurance = 650
telus = 150
enmax = 250
direct_energy = 50
fuel = 200
food = 400

total_bills = mortgage + insurance + telus + enmax + direct_energy + fuel + food

# -------------------------
# SAVINGS BUFFER
# -------------------------
st.subheader("Savings Buffer Goal")
buffer = st.number_input("Emergency Buffer Contribution", value=100)

# -------------------------
# DEBT (YOUR REAL BALANCES)
# -------------------------
rbc_mastercard = 7882
pc_mastercard = 5119
loc = 15463

st.subheader("Debt Focus")
debt_payment = st.number_input("RBC Mastercard Payment (Priority)", value=400)

# -------------------------
# CALCULATIONS
# -------------------------
remaining = total_income - total_bills - buffer - debt_payment

# -------------------------
# OUTPUT
# -------------------------
st.subheader("Summary")

st.write("Total Income:", total_income)
st.write("Total Bills:", total_bills)
st.write("Savings Buffer:", buffer)
st.write("RBC Mastercard Payment:", debt_payment)

st.markdown("---")

st.subheader("Results")

st.write("💰 Safe to Spend:", remaining)

# -------------------------
# DEBT STATUS DISPLAY
# -------------------------
st.subheader("Debt Balances")
st.write("RBC Mastercard:", rbc_mastercard - debt_payment)
st.write("PC Mastercard:", pc_mastercard)
st.write("Line of Credit:", loc)

# -------------------------
# GUIDANCE LOGIC
# -------------------------
st.markdown("---")

if remaining < 0:
    st.error("Warning: You are over budget. Adjust spending or debt payments.")
elif remaining < 300:
    st.warning("Tight budget. Be careful with spending.")
else:
    st.success("Budget looks stable.")

st.info("Priority: Pay RBC Mastercard first, then PC Mastercard, then Line of Credit.")