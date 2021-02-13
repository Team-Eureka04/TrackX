import streamlit as st
import pandas as pd

df = pd.read_csv("chrome_history.csv")
st.title("Webview App")

st.write(df)
