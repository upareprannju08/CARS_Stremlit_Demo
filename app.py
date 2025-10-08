import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

# Set Streamlit page config
st.set_page_config(page_title="Car Dataset Dashboard", layout="wide")

st.title("🚗 Car Data Analysis Dashboard")

# Load data
df = pd.read_csv("CARS.csv")

# Clean currency columns
df["MSRP"] = df["MSRP"].replace("[$,]", "", regex=True).astype("int64")
df["Invoice"] = df["Invoice"].replace("[$,]", "", regex=True).astype("int64")

# Sidebar selections
st.sidebar.header("Filter Options")

brand_list = sorted(df["Make"].unique())
brand_name = st.sidebar.selectbox("Select Car Brand:", brand_list)

brand_df = df[df["Make"] == brand_name]

type_list = sorted(brand_df["Type"].unique())
car_type = st.sidebar.selectbox("Select Car Type:", type_list)

typ = brand_df[brand_df["Type"] == car_type]

# --- 1. Bar plot of Models vs MPG_City ---
st.subheader(f"Model vs City MPG for {brand_name} ({car_type})")
fig, ax = plt.subplots(figsize=(10, 5))
sb.barplot(x=typ["Model"], y=typ["MPG_City"], ax=ax, palette="viridis")
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
st.pyplot(fig)

# --- 2. Countplots ---
st.subheader("Countplots Overview")

col1, col2 = st.columns(2)
with col1:
    st.write("### Count of Car Types")
    fig, ax = plt.subplots()
    sb.countplot(x=df["Type"], ax=ax, palette="pastel")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    st.pyplot(fig)

with col2:
    st.write("### Count of Car Makes")
    fig, ax = plt.subplots()
    sb.countplot(x=df["Make"], ax=ax, palette="muted")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    st.pyplot(fig)

# --- 3. Origin countplot ---
st.write("### Count of Car Origin")
fig, ax = plt.subplots()
sb.countplot(x=df["Origin"], ax=ax, palette="cool")
st.pyplot(fig)

# --- 4. Type vs Horsepower ---
st.write("### Horsepower by Car Type")
fig, ax = plt.subplots()
sb.barplot(x=df["Type"], y=df["Horsepower"], ax=ax, palette="rocket")
st.pyplot(fig)

# --- 5. Type vs MPG_City ---
st.write("### City Mileage by Car Type")
fig, ax = plt.subplots()
sb.barplot(x=df["Type"], y=df["MPG_City"], ax=ax, palette="cubehelix")
st.pyplot(fig)

# --- 6. DriveTrain vs MSRP ---
st.write("### MSRP by DriveTrain")
fig, ax = plt.subplots()
sb.barplot(x=df["DriveTrain"], y=df["MSRP"], ax=ax, palette="crest")
st.pyplot(fig)

# --- 7. Horsepower vs EngineSize ---
st.write("### Horsepower vs Engine Size")
fig, ax = plt.subplots()
sb.lineplot(x=df["Horsepower"], y=df["EngineSize"], ax=ax, color="teal")
st.pyplot(fig)

# --- 8. Pie charts ---
st.write("### Pie Charts")
col3, col4 = st.columns(2)
with col3:
    a = df["Origin"].value_counts()
    fig, ax = plt.subplots()
    ax.pie(a.values, labels=a.index, autopct="%d%%")
    st.pyplot(fig)

with col4:
    b = df.groupby("Type")["MSRP"].sum()
    fig, ax = plt.subplots()
    ax.pie(b.values, labels=b.index, autopct="%d%%")
    st.pyplot(fig)

# --- 9. Point and Strip plots ---
st.write("### Horsepower by DriveTrain")
fig, ax = plt.subplots()
sb.pointplot(x=df["DriveTrain"], y=df["Horsepower"], ax=ax, color="purple")
st.pyplot(fig)

st.write("### Engine Size by Origin")
fig, ax = plt.subplots()
sb.stripplot(x=df["Origin"], y=df["EngineSize"], ax=ax, palette="Set2")
st.pyplot(fig)

# --- 10. Heatmap ---
st.write("### Correlation Heatmap")
fig, ax = plt.subplots(figsize=(8, 6))
sb.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

st.success("✅ Dashboard Loaded Successfully!")

