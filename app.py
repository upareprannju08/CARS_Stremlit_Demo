import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

# Load dataset
df = pd.read_csv("CARS.csv")

# Streamlit app title
st.title("Car Horsepower Visualization")

# Brand selection
brands = df["Make"].unique()
selected_brand = st.selectbox("Select a Car Brand:", brands)

# Filter data
s = df[df["Make"] == selected_brand]

# Plot
fig, ax = plt.subplots(figsize=(10, 5))
sb.barplot(x=s["Model"], y=s["Horsepower"], ax=ax)
plt.xticks(rotation=90)
ax.set_title(f"Horsepower of {selected_brand} Models")

# Show plot
st.pyplot(fig)
