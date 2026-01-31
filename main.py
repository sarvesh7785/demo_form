import streamlit as st
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
import datetime

# ---------------- CONFIG ----------------
st.set_page_config(page_title="PD / CD Chart Viewer", layout="wide")
st.title("📊 Previous Day vs Current Day Candlestick Chart")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    df["Date_Time"] = pd.to_datetime(df["Date_Time"])
    df = df.sort_values("Date_Time")
    return df

df = load_data()

# ---------------- SIDEBAR INPUTS ----------------
st.sidebar.header("🛠 Chart Settings")

unique_dates = sorted(df["Date_Time"].dt.date.unique())

current_date = st.sidebar.selectbox(
    "Select Current Date",
    unique_dates,
    index=len(unique_dates) - 1
)

# Safety check for first date
if unique_dates.index(current_date) == 0:
    st.warning("No previous day available")
    st.stop()

prev_day = unique_dates[unique_dates.index(current_date) - 1]

# ⏰ FULL MARKET HOURS
prev_start_time = st.sidebar.time_input(
    "Previous Day Start Time",
    value=datetime.time(9, 0)
)

prev_end_time = st.sidebar.time_input(
    "Previous Day End Time",
    value=datetime.time(15, 25)
)

curr_start_time = st.sidebar.time_input(
    "Current Day Start Time",
    value=datetime.time(9, 0)
)

curr_end_time = st.sidebar.time_input(
    "Current Day End Time",
    value=datetime.time(15, 25)
)

timeframe = st.sidebar.selectbox(
    "Timeframe",
    ["1min", "5min", "15min"]
)

# 🎯 SUBMIT BUTTON
show_chart = st.sidebar.button("📈 Show Chart")

# ---------------- RESAMPLE FUNCTION ----------------
def resample_df(df, tf):
    rule = {"1min": "1T", "5min": "5T", "15min": "15T"}[tf]
    return df.resample(rule).agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum"
    }).dropna()

# ---------------- PROCESS & PLOT ----------------
if show_chart:

    prev_df = df[df["Date_Time"].dt.date == prev_day]
    curr_df = df[df["Date_Time"].dt.date == current_date]

    prev_plot = prev_df[
        (prev_df["Date_Time"].dt.time >= prev_start_time) &
        (prev_df["Date_Time"].dt.time <= prev_end_time)
    ].set_index("Date_Time")

    curr_plot = curr_df[
        (curr_df["Date_Time"].dt.time >= curr_start_time) &
        (curr_df["Date_Time"].dt.time <= curr_end_time)
    ].set_index("Date_Time")

    # ⏱ Apply timeframe
    prev_plot = resample_df(prev_plot, timeframe)
    curr_plot = resample_df(curr_plot, timeframe)

    if not prev_plot.empty and not curr_plot.empty:

        common_low = min(prev_plot["Low"].min(), curr_plot["Low"].min())
        common_high = max(prev_plot["High"].max(), curr_plot["High"].max())

        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # Previous Day
        mpf.plot(
            prev_plot,
            type="candle",
            ax=axes[0],
            style="yahoo",
            show_nontrading=True
        )
        axes[0].set_title(f"{prev_day.strftime('%d-%m-%Y')} | Previous Day")
        axes[0].set_ylim(common_low, common_high)
        axes[0].grid(True)

        # Current Day
        mpf.plot(
            curr_plot,
            type="candle",
            ax=axes[1],
            style="yahoo",
            show_nontrading=True
        )
        axes[1].set_title(f"{current_date.strftime('%d-%m-%Y')} | Current Day")
        axes[1].set_ylim(common_low, common_high)
        axes[1].grid(True)

        st.pyplot(fig)

    else:
        st.warning("⚠ No data available for selected time range")
