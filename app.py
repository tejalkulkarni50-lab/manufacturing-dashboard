import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Smart Manufacturing Dashboard", layout="wide")

st.title("🏭 Smart Manufacturing Performance Dashboard")

file = st.file_uploader("Upload Manufacturing CSV", type=["csv"])

if file is not None:
    df = pd.read_csv(file)

    # Date Conversion
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Sidebar Filters
    st.sidebar.header("Filters")

    if "Machine_ID" in df.columns:
        machine = st.sidebar.multiselect(
            "Select Machine",
            df["Machine_ID"].unique(),
            default=df["Machine_ID"].unique()
        )
        df = df[df["Machine_ID"].isin(machine)]

    if "Operation_Mode" in df.columns:
        mode = st.sidebar.multiselect(
            "Select Operation Mode",
            df["Operation_Mode"].unique(),
            default=df["Operation_Mode"].unique()
        )
        df = df[df["Operation_Mode"].isin(mode)]

    # KPI Section
    st.subheader("Key Performance Indicators")

    k1, k2, k3, k4 = st.columns(4)

    k1.metric("Avg Temp (°C)", round(df["Temperature_C"].mean(), 2))
    k2.metric("Avg Power (kW)", round(df["Power_Consumption_kW"].mean(), 2))
    k3.metric("Avg Defect (%)", round(df["Quality_Control_Defect_Rate_%"].mean(), 2))
    k4.metric("Avg Maintenance", round(df["Predictive_Maintenance_Score"].mean(), 2))

    st.markdown("---")

    # Row 1 Charts
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### Production Speed Over Time")
        if "Date" in df.columns:
            fig1, ax1 = plt.subplots(figsize=(6,4))
            ax1.plot(df["Date"], df["Production_Speed_units_per_hr"])
            ax1.set_xlabel("Date")
            ax1.set_ylabel("Production Speed")
            st.pyplot(fig1)

    with c2:
        st.markdown("### Temperature vs Error Rate")
        fig2, ax2 = plt.subplots(figsize=(6,4))
        ax2.scatter(df["Temperature_C"], df["Error_Rate_%"])
        ax2.set_xlabel("Temperature (°C)")
        ax2.set_ylabel("Error Rate (%)")
        st.pyplot(fig2)

    # Row 2 Charts
    c3, c4 = st.columns(2)

    with c3:
        st.markdown("### Efficiency Status Distribution")
        if "Efficiency_Status" in df.columns:
            fig3, ax3 = plt.subplots(figsize=(6,4))
            df["Efficiency_Status"].value_counts().plot(
                kind="bar", ax=ax3
            )
            st.pyplot(fig3)

    with c4:
        st.markdown("### Correlation Heatmap")
        numeric_df = df.select_dtypes(include=["number"])
        fig4, ax4 = plt.subplots(figsize=(6,4))
        sns.heatmap(numeric_df.corr(), ax=ax4, cmap="coolwarm")
        st.pyplot(fig4)

    st.markdown("---")

    st.subheader("Filtered Dataset Preview")
    st.dataframe(df)
