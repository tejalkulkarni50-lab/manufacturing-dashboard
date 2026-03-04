import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="AI Smart Manufacturing ELC Dashboard", layout="wide")

st.title("🏭 AI Smart Manufacturing - Complete Analytics Dashboard")

file = st.file_uploader("Upload Manufacturing CSV", type=["csv"])

if file is not None:
    df = pd.read_csv(file)

    # Date Conversion
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    st.sidebar.header("🔎 Filters")

    # Machine Filter
    if "Machine_ID" in df.columns:
        machine = st.sidebar.multiselect("Select Machine", df["Machine_ID"].unique(), default=df["Machine_ID"].unique())
        df = df[df["Machine_ID"].isin(machine)]

    # Operation Mode Filter
    if "Operation_Mode" in df.columns:
        mode = st.sidebar.multiselect("Select Operation Mode", df["Operation_Mode"].unique(), default=df["Operation_Mode"].unique())
        df = df[df["Operation_Mode"].isin(mode)]

    # KPI Section
    st.subheader("📌 Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Avg Temperature (°C)", round(df["Temperature_C"].mean(), 2))
    col2.metric("Avg Power (kW)", round(df["Power_Consumption_kW"].mean(), 2))
    col3.metric("Avg Defect Rate (%)", round(df["Quality_Control_Defect_Rate_%"].mean(), 2))
    col4.metric("Avg Maintenance Score", round(df["Predictive_Maintenance_Score"].mean(), 2))

    st.divider()

    # Production Speed Over Time
    if "Date" in df.columns:
        st.subheader("📈 Production Speed Over Time")
        fig1, ax1 = plt.subplots()
        ax1.plot(df["Date"], df["Production_Speed_units_per_hr"])
        ax1.set_xlabel("Date")
        ax1.set_ylabel("Production Speed")
        st.pyplot(fig1)

    # Temperature vs Error Rate
    st.subheader("🔥 Temperature vs Error Rate")
    fig2, ax2 = plt.subplots()
    ax2.scatter(df["Temperature_C"], df["Error_Rate_%"])
    ax2.set_xlabel("Temperature (°C)")
    ax2.set_ylabel("Error Rate (%)")
    st.pyplot(fig2)

    # Energy Efficiency vs Power
    if "Energy_Efficiency" in df.columns:
        st.subheader("⚡ Energy Efficiency vs Power Consumption")
        fig3, ax3 = plt.subplots()
        ax3.scatter(df["Power_Consumption_kW"], df["Energy_Efficiency"])
        ax3.set_xlabel("Power Consumption (kW)")
        ax3.set_ylabel("Energy Efficiency")
        st.pyplot(fig3)

    # Efficiency Status Distribution
    if "Efficiency_Status" in df.columns:
        st.subheader("📊 Efficiency Status Distribution")
        fig4, ax4 = plt.subplots()
        df["Efficiency_Status"].value_counts().plot(kind="pie", autopct="%1.1f%%", ax=ax4)
        st.pyplot(fig4)

    # Correlation Heatmap
    st.subheader("🔍 Correlation Heatmap")
    numeric_df = df.select_dtypes(include=["number"])
    fig5, ax5 = plt.subplots()
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax5)
    st.pyplot(fig5)

    st.divider()

    # Dataset Preview
    st.subheader("📂 Filtered Dataset")
    st.dataframe(df)

    # Download Button
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇ Download Filtered Data", csv, "filtered_data.csv", "text/csv")
