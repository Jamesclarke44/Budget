import streamlit as st

st.title("Simple Budget & Debt Tracker")

# -------------------------
# INCOME
# -------------------------
st.subheader("Income")

income = st.number_input("Paycheque Income", value=5200)
extra_income = st.number_input("Overtime / Extra Income", value=0)

total_income = income + extra_income

# -------------------------
# MONTHLY BILLS (EDITABLE)
# -------------------------
st.subheader("Monthly Bills")

mortgage = st.number_input("Mortgage", value=3260)
insurance = st.number_input("Insurance", value=650)
telus = st.number_input("Telus", value=150)
enmax = st.number_input("ENMAX", value=250)
direct_energy = st.number_input("Direct Energy", value=50)
fuel = st.number_input("Fuel", value=200)
food = st.number_input("Food", value=400)

total_bills = (
    mortgage +
    insurance +
    telus +
    enmax +
    direct_energy +
    fuel +
    food
)

# -------------------------
# SAVINGS BUFFER
# -------------------------
st.subheader("Savings Buffer")

buffer = st.number_input("Emergency Buffer Contribution", value=100)

# -------------------------
# DEBT (YOUR ACTUAL BALANCES)
# -------------------------
st.subheader("Debt Balances")

rbc_mastercard = 7882
pc_mastercard = 5119
loc = 15463

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

st.metric("💰 Safe to Spend", f"${remaining:.2f}")

# -------------------------
# DEBT STATUS
# -------------------------
st.subheader("Debt Overview")

st.write("RBC Mastercard Remaining:", rbc_mastercard - debt_payment)
st.write("PC Mastercard:", pc_mastercard)
st.write("Line of Credit:", loc)

# -------------------------
# WARNINGS
# -------------------------
st.markdown("---")

if remaining < 0:
    st.error("You are over budget. Adjust spending or debt payments.")
elif remaining < 300:
    st.warning("Tight budget. Be careful with spending.")
else:
    st.success("Budget is stable.")

st.info("Priority order: RBC Mastercard → PC Mastercard → Line of Credit")