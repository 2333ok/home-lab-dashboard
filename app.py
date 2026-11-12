import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Home Lab Dashboard", page_icon="🛰️", layout="wide")
st.title("🛰️ Home Lab Dashboard")
st.caption("Demo app for Streamlit Community Cloud — swap the sample data for your own source.")

@st.cache_data
def load():
    rng = np.random.default_rng(7)
    days = pd.date_range("2026-10-01", periods=42, freq="D")
    return pd.DataFrame({
        "date": days,
        "cpu": rng.normal(38, 9, len(days)).clip(0, 100).round(1),
        "mem": rng.normal(61, 7, len(days)).clip(0, 100).round(1),
        "net_gb": rng.gamma(2.0, 3.5, len(days)).round(1),
    })

df = load()
c1, c2, c3 = st.columns(3)
c1.metric("Avg CPU", f"{df.cpu.mean():.1f} %")
c2.metric("Avg Memory", f"{df.mem.mean():.1f} %")
c3.metric("Traffic (42d)", f"{df.net_gb.sum():.0f} GB")

tab1, tab2 = st.tabs(["Trend", "Raw data"])
with tab1:
    st.line_chart(df.set_index("date")[["cpu", "mem"]])
    st.bar_chart(df.set_index("date")["net_gb"])
with tab2:
    st.dataframe(df, use_container_width=True, hide_index=True)

with st.sidebar:
    st.header("Filters")
    lo, hi = st.slider("CPU range", 0, 100, (0, 100))
    st.write(f"Rows in range: {int(df.cpu.between(lo, hi).sum())}")
