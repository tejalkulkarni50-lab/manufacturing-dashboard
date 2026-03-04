import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Manufacturing Efficiency Dashboard", layout="wide")
st.title("🏭 Manufacturing Efficiency Prediction Dashboard")

# ---------------- UPLOAD DATA ---------------- #
file = st.file_uploader("Upload CSV File", type=["csv"])

if file is not None:
    df = pd.read_csv(file)

    # ---------------- DATE CONVERSION ---------------- #
    for col in df.columns:
        if "date" in col.lower() or "time" in col.lower():
            try:
                df[col] = pd.to_datetime(df[col], errors="coerce")
            except:
                pass

    # ---------------- SIDEBAR FILTERS ---------------- #
    st.sidebar.header("Filters")
    if "Machine_ID" in df.columns:
        machines = st.sidebar.multiselect(
            "Select Machines",
            options=df["Machine_ID"].unique(),
            default=df["Machine_ID"].unique()
        )
        df = df[df["Machine_ID"].isin(machines)]

    if "Operation_Mode" in df.columns:
        op_modes = st.sidebar.multiselect(
            "Select Operation Mode",
            options=df["Operation_Mode"].unique(),
            default=df["Operation_Mode"].unique()
        )
        df = df[df["Operation_Mode"].isin(op_modes)]

    if "Network_Latency_ms" in df.columns:
        latency_range = st.sidebar.slider(
            "Network Latency (ms)",
            float(df["Network_Latency_ms"].min()),
            float(df["Network_Latency_ms"].max()),
            (float(df["Network_Latency_ms"].min()), float(df["Network_Latency_ms"].max()))
        )
        df = df[(df["Network_Latency_ms"] >= latency_range[0]) & (df["Network_Latency_ms"] <= latency_range[1])]

    st.sidebar.success("Filters applied ✅")

    # ---------------- KPIs ---------------- #
    st.subheader("📌 Key Performance Indicators (KPIs)")

    kpi_cols = st.columns(4)

    if "Efficiency_Class" in df.columns:
        kpi_cols[0].metric("Efficiency Class", df["Efficiency_Class"].mode()[0])
    if "Prediction_Confidence" in df.columns:
        kpi_cols[1].metric("Prediction Confidence", round(df["Prediction_Confidence"].mean(),2))
    if "Feature_Contribution" in df.columns:
        kpi_cols[2].metric("Top Feature Contribution", df["Feature_Contribution"].mode()[0])
    if "Machine_Efficiency_Profile" in df.columns:
        kpi_cols[3].metric("Machine Efficiency Profile", df["Machine_Efficiency_Profile"].mode()[0])

    st.divider()

    # ---------------- DASHBOARD TABS ---------------- #
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Efficiency Prediction",
        "🛠 Machine-Level Insights",
        "🧩 Explainability Panel",
        "⚙ Operational Monitoring"
    ])

    # -------- TAB 1: Efficiency Prediction -------- #
    with tab1:
        st.subheader("Real-Time Efficiency Classification")
        if "Efficiency_Class" in df.columns:
            counts = df["Efficiency_Class"].value_counts()
            fig1, ax1 = plt.subplots(figsize=(7,4))
            counts.plot(kind="bar", ax=ax1, color=["green","orange","red"])
            ax1.set_xlabel("Efficiency Class")
            ax1.set_ylabel("Count")
            st.pyplot(fig1)

        if "Prediction_Confidence" in df.columns:
            st.subheader("Prediction Confidence Score")
            fig2, ax2 = plt.subplots(figsize=(7,4))
            df["Prediction_Confidence"].hist(ax=ax2, bins=20, color="skyblue")
            ax2.set_xlabel("Confidence")
            ax2.set_ylabel("Frequency")
            st.pyplot(fig2)

    # -------- TAB 2: Machine-Level Insights -------- #
    with tab2:
        st.subheader("Efficiency Trends per Machine")
        if "Machine_ID" in df.columns and "Efficiency_Class" in df.columns:
            fig3, ax3 = plt.subplots(figsize=(7,4))
            sns.countplot(x="Machine_ID", hue="Efficiency_Class", data=df, ax=ax3)
            ax3.set_ylabel("Count")
            st.pyplot(fig3)

        st.subheader("Historical Classification Patterns")
        if "Date" in df.columns and "Efficiency_Class" in df.columns:
            fig4, ax4 = plt.subplots(figsize=(7,4))
            df_group = df.groupby(["Date","Efficiency_Class"]).size().unstack(fill_value=0)
            df_group.plot(ax=ax4)
            st.pyplot(fig4)

    # -------- TAB 3: Explainability Panel -------- #
    with tab3:
        st.subheader("Feature Importance")
        if "Feature_Contribution" in df.columns:
            feature_counts = df["Feature_Contribution"].value_counts().head(10)
            fig5, ax5 = plt.subplots(figsize=(7,4))
            feature_counts.plot(kind="barh", ax=ax5, color="purple")
            ax5.set_xlabel("Importance Count")
            ax5.set_ylabel("Feature")
            st.pyplot(fig5)

        st.subheader("Why Efficiency Dropped/Improved")
        st.write("Insights based on top feature contributions per prediction. (Sample Explanation)")

    # -------- TAB 4: Operational Monitoring -------- #
    with tab4:
        st.subheader("Efficiency by Operation Mode")
        if "Operation_Mode" in df.columns and "Efficiency_Class" in df.columns:
            fig6, ax6 = plt.subplots(figsize=(7,4))
            sns.countplot(x="Operation_Mode", hue="Efficiency_Class", data=df, ax=ax6)
            st.pyplot(fig6)

        st.subheader("Network vs Sensor Impact")
        if "Network_Latency_ms" in df.columns and "Temperature_C" in df.columns:
            fig7, ax7 = plt.subplots(figsize=(7,4))
            ax7.scatter(df["Network_Latency_ms"], df["Temperature_C"], c="blue")
            ax7.set_xlabel("Network Latency (ms)")
            ax7.set_ylabel("Temperature (C)")
            st.pyplot(fig7)

    # ---------------- DOWNLOAD DATA ---------------- #
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇ Download Filtered Data", csv, "filtered_data.csv", "text/csv")
