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



with st.sidebar:
    st.title("Option Profit and Loss Diagram")
    linkedin_url = "https://www.linkedin.com/in/charliewarburton-cambridge/"
    st.markdown(f'<a href="{linkedin_url}" target="_blank" style="text-decoration: none; color: inherit;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" height="25" style="vertical-align: middle; margin-right: 10px;">`Charlie Warburton`</a>', unsafe_allow_html=True)

    #current_price = st.number_input("Current Asset Price", value=100.0)