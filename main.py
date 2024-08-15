import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go
from numpy import log, sqrt, exp
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(
    page_title="Option Profit and Loss Diagram",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded")

class Call:
    def __init__(self, strike, premium):
        self.strike = float(strike)
        self.premium = float(premium)
        
    def payoff(self, spot):
        return max(spot - self.strike, 0) - self.premium # if spot is less than strike then cost is just premium
    def breakeven(self):
        return self.strike + self.premium

class Put:
    def __init__(self, strike, premium):
        self.strike = float(strike)
        self.premium = float(premium)

    def payoff(self, spot):
        return max(self.strike - spot, 0) - self.premium # If spot is above strike then don't use option and cost is premium
    def breakeven(self):
        return self.strike - self.premium
        
class Strategy:
    def __init__(self):
        # To contain the bought and written contracts
        self.long = []
        self.short = []
    
    def buy(self, contract):
        self.long.append(contract)
    def write(self, contract):
        self.short.append(contract)
    
    def strikes(self): 
        # To get unique list of strike prices for x axis (set doesn't allow duplictes)
        unique_strikes = set([c.strike for c in self.long + self.short]) 
        return sorted(list(set(unique_strikes)))
    
    # PnL for given spot price (Observation in y axis)
    def single_pnl(self, spot):
        profit = sum(c.payoff(spot) for c in self.long)
        # If the contracts we sold are in profit then its a loss
        loss = sum(c.payoff(spot) for c in self.short)

        return profit - loss
    
    # List of PnLs for each spot price (Series for Y axis)
    def list_pnl(self, spots):
        return list(map(self.single_pnl, spots))
    
    # The spot prices that PnL needs to be computed for
    # Note max spot price is 1000000 (saves dealing with infinity)
    def _spots(self):
        return [0, *self.strikes, 1000000]
    
    
    

    



with st.sidebar:
    st.title("Option Profit and Loss Diagram")
    linkedin_url = "https://www.linkedin.com/in/charliewarburton-cambridge/"
    st.markdown(f'<a href="{linkedin_url}" target="_blank" style="text-decoration: none; color: inherit;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" height="25" style="vertical-align: middle; margin-right: 10px;">`Charlie Warburton`</a>', unsafe_allow_html=True)

    #current_price = st.number_input("Current Asset Price", value=100.0)