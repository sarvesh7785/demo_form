import streamlit as st
import math

st.set_page_config(page_title="EMI Calculator", layout="centered")

st.title("💰 EMI Calculator")

# User Inputs
loan_amount = st.number_input("Loan Amount (₹)", min_value=1000, value=500000, step=1000)
annual_interest = st.number_input("Annual Interest Rate (%)", min_value=0.1, value=8.5, step=0.1)
tenure_years = st.number_input("Loan Tenure (Years)", min_value=1, value=20, step=1)

# Convert values
monthly_interest = annual_interest / (12 * 100)
tenure_months = tenure_years * 12

# EMI Calculation
if monthly_interest > 0:
    emi = (loan_amount * monthly_interest * (1 + monthly_interest) ** tenure_months) / \
          ((1 + monthly_interest) ** tenure_months - 1)
else:
    emi = loan_amount / tenure_months

total_payment = emi * tenure_months
total_interest = total_payment - loan_amount

# Display Results
st.subheader("📊 EMI Details")
st.success(f"Monthly EMI: ₹ {emi:,.2f}")
st.write(f"**Total Interest Payable:** ₹ {total_interest:,.2f}")
st.write(f"**Total Amount Payable:** ₹ {total_payment:,.2f}")
