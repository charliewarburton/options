import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go
from numpy import log, sqrt, exp
import matplotlib.pyplot as plt
import seaborn as sns
from options import Strategy, Call, Put

# Page configuration
st.set_page_config(
    page_title="Option Profit and Loss Diagram",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded")

# Initialise strategy session state on first run
if 'strategy' not in st.session_state:
    st.session_state.strategy = Strategy()

def add_contract(buy_write, call_put, strike_price, premium_val):
    s = st.session_state.strategy
    if buy_write == "Buy":
        if call_put == "Call":
            s.buy(Call(strike = strike_price, premium = premium_val))
        else:
            s.buy(Put(strike = strike_price, premium = premium_val))
    else:
        if call_put == "Call":
            s.write(Call(strike = strike_price, premium = premium_val))
        else:
            s.write(Put(strike = strike_price, premium = premium_val))


with st.sidebar:
    st.title("Option Profit and Loss Diagram")
    linkedin_url = "https://www.linkedin.com/in/charliewarburton-cambridge/"
    st.markdown(f'<a href="{linkedin_url}" target="_blank" style="text-decoration: none; color: inherit;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" height="25" style="vertical-align: middle; margin-right: 10px;">`Charlie Warburton`</a>', unsafe_allow_html=True)

    #current_price = st.number_input("Current Asset Price", value=100.0)
    st.write("--------------------------------------")

    

    buy_write = st.selectbox(
        label="Buy or Write?",
        options=list(["Buy", "Write"])
    )
    call_put = st.selectbox(
        label = "Call or Put?",
        options=list(["Call", "Put"])
    )
    strike_price = st.number_input("Enter strike price",
                                    min_value = 0.00, max_value = 100000.00,
                                    value = 100.00,
                                    step = 0.01)
    premium_val = st.number_input("Enter the premium",
                                min_value = 0.01, max_value = 100.00,
                                value = 5.00,
                                step = 0.01)
    
    st.session_state.buy_write = buy_write
    st.session_state.call_put = call_put
    st.session_state.strike_price = strike_price
    st.session_state.premium_val = premium_val

    if st.button("Add contract"):
        add_contract(buy_write, call_put, strike_price, premium_val)
        st.success("Contract added successfully!")

s = st.session_state.strategy
if st.checkbox("Show current strategy"):
    for contract in s.long:
        st.write(f"Long: {type(contract).__name__} - Strike: {round(contract.strike, 3)}, Premium: {round(contract.premium, 3)}")
    for contract in s.short:
        st.write(f"Short: {type(contract).__name__} - Strike: {round(contract.strike, 3)}, Premium: {round(contract.premium, 3)}")

if len(s.long) or len(s.short) != 0:
    fig = s.plot()
    st.pyplot(fig)
