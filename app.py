import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dynamic Smart Analytics Dashboard", layout="wide")

st.title("🏭 Dynamic Manufacturing Analytics Dashboard")

file = st.file_uploader("Upload CSV File", type=["csv"])

if file is not None:

    df = pd.read_csv(file)

    # Auto detect date columns safely
    for col in df.columns:
        try:
            df[col] = pd.to_datetime(df[col])
        except:
            pass

    st.sidebar.header("🔎 Dynamic Filters")

    # Dynamic Filters for categorical columns
    categorical_cols = df.select_dtypes(include=["object"]).columns
    for col in categorical_cols:
        options = df[col].dropna().unique()
        selected = st.sidebar.multiselect(
            f"Filter {col}",
            options,
            default=options
        )
        df = df[df[col].isin(selected)]

    st.sidebar.success("Filters Applied ✅")

    # ---------------- KPIs (SAFE VERSION) ---------------- #
    st.subheader("📌 Auto KPI Section")

    numeric_cols = df.select_dtypes(include=["number"]).columns

    if len(numeric_cols) > 0:
        num_kpis = min(4, len(numeric_cols))
        kpi_cols = st.columns(num_kpis)

        for i in range(num_kpis):
            col_name = numeric_cols[i]
            kpi_cols[i].metric(
                f"Avg {col_name}",
                round(df[col_name].mean(), 2)
            )
    else:
        st.warning("No Numeric Columns Available for KPI")

    st.divider()

    # ---------------- AUTO DASHBOARDS ---------------- #

    tab1, tab2, tab3 = st.tabs([
        "📈 Trend Analysis",
        "📊 Distribution Analysis",
        "🔍 Correlation & Data"
    ])

    # -------- TAB 1 (Trend Analysis) -------- #
    with tab1:
        date_cols = df.select_dtypes(include=["datetime64[ns]"]).columns

        if len(date_cols) > 0 and len(numeric_cols) > 0:
            selected_date = st.selectbox("Select Date Column", date_cols)
            selected_numeric = st.selectbox("Select Numeric Column", numeric_cols)

            fig, ax = plt.subplots(figsize=(7,4))   # Medium size
            ax.plot(df[selected_date], df[selected_numeric])
            ax.set_xlabel(selected_date)
            ax.set_ylabel(selected_numeric)
            st.pyplot(fig)
        else:
            st.info("No Date Column Detected")

    # -------- TAB 2 (Distribution) -------- #
    with tab2:
        selected_col = st.selectbox("Select Column for Distribution", df.columns)

        fig2, ax2 = plt.subplots(figsize=(7,4))   # Medium size

        if selected_col in numeric_cols:
            df[selected_col].hist(ax=ax2)
        else:
            df[selected_col].value_counts().plot(kind="bar", ax=ax2)

        ax2.set_title(f"Distribution of {selected_col}")
        st.pyplot(fig2)

    # -------- TAB 3 (Correlation + Data View) -------- #
    with tab3:
        if len(numeric_cols) > 1:
            st.subheader("Correlation Heatmap")
            fig3, ax3 = plt.subplots(figsize=(7,4))   # Medium size
            sns.heatmap(
                df[numeric_cols].corr(),
                cmap="coolwarm",
                annot=False,
                ax=ax3
            )
            st.pyplot(fig3)

        st.subheader("Filtered Dataset")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇ Download Filtered Data",
            csv,
            "filtered_data.csv",
            "text/csv"
        )
