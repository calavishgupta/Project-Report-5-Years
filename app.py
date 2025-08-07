import streamlit as st
from scheme_data import schemes

st.set_page_config(page_title="Schemes Dashboard", layout="wide")
st.title("Schemes Dashboard")

# Sidebar: List of main scheme names
st.sidebar.header("Scheme Groups")
main_scheme_names = list(schemes.keys())
selected_main_scheme = st.sidebar.selectbox("Select a Scheme Group", main_scheme_names)

# Main dashboard area: show grouped schemes and details
st.header(selected_main_scheme)
variants = schemes[selected_main_scheme]

for i, variant in enumerate(variants, 1):
    with st.expander(f"Variant {i}: {variant.get('Eligible Category', '')}"):
        cols = st.columns(2)
        for idx, (key, value) in enumerate(variant.items()):
            with cols[idx % 2]:
                st.markdown(f"**{key}:** {value if value is not None else '-'}")
