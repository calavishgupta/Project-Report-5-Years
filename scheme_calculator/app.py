import streamlit as st
from .schemes_data import get_scheme_data
from .calculator_logic import calculate_benefit

def main():
    st.header("🧮 Government Scheme Benefit Calculator")
    st.markdown(
        "Select a scheme and enter your details to estimate your benefit. "
        "For more information on each scheme, see the info section below."
    )
    st.divider()

    schemes = get_scheme_data("schemes.csv")
    scheme_names = list(schemes.keys())
    cols = st.columns([2, 1])
    with cols[0]:
        selected_scheme = st.selectbox("**Choose Scheme**", scheme_names, help="Pick the scheme you want to estimate benefits for.")
    with cols[1]:
        st.info(schemes[selected_scheme]["Description"])

    with st.expander("ℹ️ Scheme Eligibility & Formula", expanded=False):
        st.write(schemes[selected_scheme]["Eligibility"])
        st.code(f"Formula: {schemes[selected_scheme]['Calculation']}")

    st.subheader("🔢 Your Details")
    input_cols = st.columns(2)
    age = input_cols[0].number_input("Age", min_value=0, max_value=120, value=30, help="Enter your age")
    income = input_cols[1].number_input("Annual Income (₹)", min_value=0, value=500000, help="Your yearly income")
    additional = st.text_input("Any other info (optional)", placeholder="e.g., special conditions")

    if st.button("Calculate"):
        result = calculate_benefit(selected_scheme, age, income, additional, schemes)
        if isinstance(result, str) and "error" in result.lower():
            st.error(result)
        else:
            st.success(f"🎉 Estimated Benefit: ₹{result:,}")
