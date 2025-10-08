import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Car Dashboard", layout="wide")
st.title("🚗 Car Dataset Dashboard")

# Load data
df = pd.read_csv("CARS.csv")
df["MSRP"] = df["MSRP"].replace("[$,]", "", regex=True).astype("int64")
df["Invoice"] = df["Invoice"].replace("[$,]", "", regex=True).astype("int64")

# Sidebar for filters
st.sidebar.header("Filter Options")
brand_list = sorted(df["Make"].unique())
brand_name = st.sidebar.selectbox("Select Car Brand:", brand_list)

brand_df = df[df["Make"] == brand_name]
type_list = sorted(brand_df["Type"].unique())
car_type = st.sidebar.selectbox("Select Car Type:", type_list)
typ = brand_df[brand_df["Type"] == car_type]

# ===== FRAME 1: Brand & Type Analysis =====
st.header("📊 Brand & Type Analysis")
frame1_col1, frame1_col2 = st.columns(2)

with frame1_col1:
    st.subheader("Model vs City MPG")
    fig, ax = plt.subplots(figsize=(8, 5))
    sb.barplot(x=typ["Model"], y=typ["MPG_City"], ax=ax, palette="viridis")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    st.pyplot(fig)

with frame1_col2:
    st.subheader("Horsepower vs Engine Size")
    fig, ax = plt.subplots(figsize=(8, 5))
    sb.lineplot(x=df["Horsepower"], y=df["EngineSize"], ax=ax, color="teal")
    st.pyplot(fig)

# ===== FRAME 2: Overall Dataset Insights =====
st.header("📈 Overall Dataset Insights")
frame2_col1, frame2_col2 = st.columns(2)

with frame2_col1:
    st.subheader("Count of Car Types")
    fig, ax = plt.subplots()
    sb.countplot(x=df["Type"], ax=ax, palette="pastel")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    st.pyplot(fig)

    st.subheader("Count of Car Origin")
    fig, ax = plt.subplots()
    sb.countplot(x=df["Origin"], ax=ax, palette="cool")
    st.pyplot(fig)

    st.subheader("Origin Distribution (Pie)")
    origin_counts = df["Origin"].value_counts()
    fig, ax = plt.subplots()
    ax.pie(origin_counts.values, labels=origin_counts.index, autopct="%d%%")
    st.pyplot(fig)

with frame2_col2:
    st.subheader("MSRP by DriveTrain")
    fig, ax = plt.subplots()
    sb.barplot(x=df["DriveTrain"], y=df["MSRP"], ax=ax, palette="crest")
    st.pyplot(fig)

    st.subheader("Horsepower by DriveTrain")
    fig, ax = plt.subplots()
    sb.pointplot(x=df["DriveTrain"], y=df["Horsepower"], ax=ax, color="purple")
    st.pyplot(fig)

    st.subheader("Type-wise MSRP Distribution (Pie)")
    type_msrp = df.groupby("Type")["MSRP"].sum()
    fig, ax = plt.subplots()
    ax.pie(type_msrp.values, labels=type_msrp.index, autopct="%d%%")
    st.pyplot(fig)

# ===== FRAME 3: Heatmap =====
st.header("🟢 Correlation Heatmap")
fig, ax = plt.subplots(figsize=(10, 6))
sb.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

st.success("✅ Dashboard Loaded Successfully!")


