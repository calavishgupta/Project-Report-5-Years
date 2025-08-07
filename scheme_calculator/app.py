import streamlit as st
from schemes_data import get_scheme_data
from calculator_logic import calculate_benefit

def main():
    st.title("Scheme Calculator")
    st.write("Select a scheme and enter your details to calculate your benefit.")

    schemes = get_scheme_data("schemes.csv")
    selected_scheme = st.selectbox("Choose Scheme", list(schemes.keys()))

    st.write("Fill your details below:")
    age = st.number_input("Age", min_value=0, max_value=120, value=30)
    income = st.number_input("Annual Income (₹)", min_value=0, value=500000)
    additional = st.text_input("Any other info (optional)")

    if st.button("Calculate"):
        result = calculate_benefit(selected_scheme, age, income, additional, schemes)
        st.success(f"Estimated Benefit: {result}")

if __name__ == "__main__":
    main()