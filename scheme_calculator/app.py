# Scheme Calculator

import streamlit as st
import pandas as pd

# Load the schemes data
schemes_data = pd.read_csv('schemes.csv')

def display_scheme(scheme):
    st.write(f"## {scheme['Name']}")
    st.write(scheme['Description'])

st.title('Scheme Calculator')

for index, scheme in schemes_data.iterrows():
    if st.checkbox(scheme['Name']):
        display_scheme(scheme)