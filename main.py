import streamlit as st

st.set_page_config(page_title="My First Streamlit App")

st.title("👋 Hello Amrita")
st.write("This is a simple Streamlit app")

name = st.text_input("Enter your name")

if name:
    st.success(f"Welcome, {name}!")

number = st.slider("Pick a number", 0, 100, 50)

st.write("You selected:", number)
