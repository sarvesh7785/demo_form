import streamlit as st

st.title("Simple Streamlit Form")

with st.form("my_form"):
    name = st.text_input("Enter your name")
    age = st.number_input("Enter your age", min_value=0, max_value=120)
    submitted = st.form_submit_button("Submit")

if submitted:
    st.success("Form submitted successfully!")
    st.write("Name:", name)
    st.write("Age:", age)
