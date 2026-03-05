import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Page config
st.set_page_config(page_title="Manufacturing Efficiency AI Dashboard", layout="wide")
st.title("🏭 AI-Based Manufacturing Efficiency Dashboard")

# ===== Dataset Load =====
@st.cache_data
def load_data():
    df = pd.read_csv("Thlaes_Group_Manufacturing.csv")  # Auto-load your dataset
    return df

df = load_data()

# ===== Dataset Preview =====
st.subheader("Dataset Preview")
st.dataframe(df.head())

# ===== Dataset Summary =====
st.subheader("Dataset Summary")
st.write(df.describe())

# ===== KPI SECTION =====
st.subheader("Key Performance Indicators")
col1, col2, col3 = st.columns(3)

if "Production_Speed_units_per_hr" in df.columns:
    col1.metric("Total Production", int(df["Production_Speed_units_per_hr"].sum()))

if "Error_Rate_%" in df.columns:
    col2.metric("Average Error Rate", round(df["Error_Rate_%"].mean(),2))

if "Efficiency_Stattus" in df.columns:
    high_eff = (df["Efficiency_Stattus"]=="High").sum()
    col3.metric("High Efficiency Machines", high_eff)

# ===== Efficiency Class Distribution =====
st.subheader("Efficiency Class Distribution")
if "Efficiency_Stattus" in df.columns:
    fig = px.histogram(df, x="Efficiency_Stattus", color="Efficiency_Stattus",
                       color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig, use_container_width=True)

# ===== Production Trend =====
st.subheader("Production Trend")
if "Production_Speed_units_per_hr" in df.columns:
    fig, ax = plt.subplots()
    df["Production_Speed_units_per_hr"].plot(ax=ax, color="#1f77b4")
    ax.set_xlabel("Index")
    ax.set_ylabel("Production Units per Hour")
    st.pyplot(fig)

# ===== Sensor Data Distribution =====
st.subheader("Sensor Value Distribution")
if "Temperature_C" in df.columns:
    fig, ax = plt.subplots()
    sns.histplot(df["Temperature_C"], kde=True, color="#ff7f0e", ax=ax)
    st.pyplot(fig)

# ===== Feature Correlation Heatmap =====
st.subheader("Feature Correlation Heatmap")
fig, ax = plt.subplots(figsize=(8,5))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

# ===== AI Model Prediction =====
st.subheader("AI Efficiency Prediction Model")
if "Efficiency_Stattus" in df.columns:
    df_clean = df.dropna()
    X = df_clean.select_dtypes(include=['int64','float64'])
    y = df_clean["Efficiency_Stattus"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    acc = accuracy_score(y_test, pred)
    st.success(f"Model Accuracy: {round(acc*100,2)} %")

    # Feature Importance
    st.subheader("Feature Importance")
    feat_importance = pd.DataFrame({
        "Feature": X.columns,
        "Importance": model.feature_importances_
    }).sort_values(by="Importance", ascending=False)

    fig, ax = plt.subplots(figsize=(8,4))
    sns.barplot(x="Importance", y="Feature", data=feat_importance, palette="Set2", ax=ax)
    st.pyplot(fig)
