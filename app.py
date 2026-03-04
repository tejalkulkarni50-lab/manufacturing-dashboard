import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Manufacturing Analytics", layout="wide")

st.title("🏭 AI Manufacturing Efficiency & Predictive Analytics Dashboard")

file = st.file_uploader("Upload Manufacturing CSV", type=["csv"])

if file is not None:
    df = pd.read_csv(file)

    # Convert Date
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    st.subheader("📊 Dataset Overview")
    st.dataframe(df.head())

    st.subheader("📈 Statistical Summary")
    st.write(df.describe())

    # Sidebar Filters
    st.sidebar.header("Filter Data")

    if "Machine_ID" in df.columns:
        machine = st.sidebar.selectbox("Select Machine", df["Machine_ID"].unique())
        df = df[df["Machine_ID"] == machine]

    if "Operation_Mode" in df.columns:
        mode = st.sidebar.selectbox("Select Operation Mode", df["Operation_Mode"].unique())
        df = df[df["Operation_Mode"] == mode]

    # KPI Section
    st.subheader("📌 Key Performance Indicators")

    col1, col2, col3 = st.columns(3)

    col1.metric("Avg Temperature (°C)", round(df["Temperature_C"].mean(), 2))
    col2.metric("Avg Power Consumption (kW)", round(df["Power_Consumption_kW"].mean(), 2))
    col3.metric("Avg Defect Rate (%)", round(df["Quality_Control_Defect_Rate_%"].mean(), 2))

    # Line Chart
    st.subheader("📉 Production Speed Over Time")

    if "Date" in df.columns:
        fig, ax = plt.subplots()
        ax.plot(df["Date"], df["Production_Speed_units_per_hr"])
        ax.set_xlabel("Date")
        ax.set_ylabel("Production Speed")
        st.pyplot(fig)

    # Correlation
    st.subheader("🔍 Correlation Matrix")
    st.write(df.corr(numeric_only=True))
