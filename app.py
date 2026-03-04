import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Manufacturing Dashboard", layout="wide")

st.title("📊 AI Manufacturing Efficiency Dashboard")

file = st.file_uploader("Upload your CSV file", type=["csv"])

if file is not None:
    df = pd.read_csv(file)

    st.subheader("Dataset Preview")
    st.dataframe(df)

    st.subheader("Basic Statistics")
    st.write(df.describe())

    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns

    if len(numeric_cols) > 0:
        col = st.selectbox("Select Column for Chart", numeric_cols)

        fig, ax = plt.subplots()
        df[col].plot(kind='line', ax=ax)
        st.pyplot(fig)
