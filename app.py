import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os


# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Premium Car Analytics Dashboard",
    page_icon="🚘",
    layout="wide"
)


# ----------------------------
# Dark Blue Premium Theme
# ----------------------------
st.markdown("""
<style>

.stApp {
    background-color: #050816;
    color: white;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#000000,#001f3f);
}

h1, h2, h3 {
    color: #00BFFF;
    text-align: center;
    font-weight: bold;
}

[data-testid="stMetric"] {
    background: #071425;
    border: 1px solid #00BFFF;
    border-radius: 15px;
    padding: 15px;
    box-shadow: 0 0 15px #00BFFF;
}

</style>
""", unsafe_allow_html=True)


# ----------------------------
# Load Dataset
# ----------------------------
df = pd.read_csv("CARS.csv")


# Clean Price Columns
df["MSRP"] = (
    df["MSRP"]
    .replace("[$,]", "", regex=True)
    .astype(int)
)

df["Invoice"] = (
    df["Invoice"]
    .replace("[$,]", "", regex=True)
    .astype(int)
)


# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.title("🔎 Filter Cars")

brand_list = sorted(df["Make"].unique())

brand = st.sidebar.selectbox(
    "Select Car Brand",
    brand_list
)


brand_df = df[df["Make"] == brand]


type_list = sorted(
    brand_df["Type"].unique()
)

car_type = st.sidebar.selectbox(
    "Select Car Type",
    type_list
)


filtered_df = brand_df[
    brand_df["Type"] == car_type
]


# ----------------------------
# Brand Logo & Heading
# ----------------------------
logo_path = f"logos/{brand}.png"

logo_col, title_col = st.columns([1,4])

with logo_col:
    if os.path.exists(logo_path):
        st.image(
            logo_path,
            width=140
        )

with title_col:
    st.markdown(
        f"<h1>{brand} Car Analytics Dashboard</h1>",
        unsafe_allow_html=True
    )


# ============================
# Overall Market Overview
# ============================

st.header("🌎 Overall Market Overview")

o1, o2, o3, o4 = st.columns(4)

o1.metric(
    "🚗 Total Cars",
    len(df)
)

o2.metric(
    "🏢 Total Brands",
    df["Make"].nunique()
)

o3.metric(
    "⚙ Avg Horsepower",
    f"{int(df['Horsepower'].mean())} HP"
)

o4.metric(
    "💰 Highest Market Price",
    f"${df['MSRP'].max():,}"
)


# ============================
# Selected Brand Overview
# ============================

st.header(f"🚘 {brand} Brand Overview")

m1, m2, m3, m4 = st.columns(4)


m1.metric(
    "🚗 Total Models",
    len(brand_df)
)


m2.metric(
    "🚘 Car Types",
    brand_df["Type"].nunique()
)


m3.metric(
    "⚙ Avg Horsepower",
    f"{int(brand_df['Horsepower'].mean())} HP"
)


m4.metric(
    "💰 Highest Price",
    f"${brand_df['MSRP'].max():,}"
)


# Dark Chart Theme
plt.style.use("dark_background")


# ============================
# Brand Performance
# ============================

st.header("📊 Brand Performance")

col1, col2 = st.columns(2)


with col1:

    fig, ax = plt.subplots(
        figsize=(8,5)
    )

    sns.barplot(
        data=filtered_df,
        x="Model",
        y="MPG_City",
        palette="Blues",
        ax=ax
    )

    ax.set_title("City MPG by Model")

    plt.xticks(rotation=90)

    st.pyplot(fig)



with col2:

    fig, ax = plt.subplots(
        figsize=(8,5)
    )

    sns.scatterplot(
        data=brand_df,
        x="Horsepower",
        y="EngineSize",
        hue="Type",
        ax=ax
    )

    ax.set_title(
        "Horsepower vs Engine Size"
    )

    st.pyplot(fig)



# ============================
# Market Insights
# ============================

st.header("📈 Market Insights")


col3, col4 = st.columns(2)


with col3:

    fig, ax = plt.subplots()

    sns.countplot(
        data=brand_df,
        x="Type",
        palette="winter",
        ax=ax
    )

    ax.set_title(
        "Available Car Types"
    )

    plt.xticks(rotation=45)

    st.pyplot(fig)


    fig, ax = plt.subplots()

    origin = df["Origin"].value_counts()

    ax.pie(
        origin.values,
        labels=origin.index,
        autopct="%1.1f%%"
    )

    ax.set_title(
        "Car Origin Distribution"
    )

    st.pyplot(fig)



with col4:

    fig, ax = plt.subplots()

    sns.barplot(
        data=brand_df,
        x="DriveTrain",
        y="MSRP",
        palette="cool",
        ax=ax
    )

    ax.set_title(
        "Price by DriveTrain"
    )

    st.pyplot(fig)


    fig, ax = plt.subplots()

    sns.pointplot(
        data=brand_df,
        x="DriveTrain",
        y="Horsepower",
        color="cyan",
        ax=ax
    )

    ax.set_title(
        "Horsepower by DriveTrain"
    )

    st.pyplot(fig)



# ============================
# Correlation Heatmap
# ============================

st.header("🔥 Correlation Heatmap")


fig, ax = plt.subplots(
    figsize=(12,6)
)


sns.heatmap(
    brand_df.corr(numeric_only=True),
    annot=True,
    cmap="Blues",
    ax=ax
)

st.pyplot(fig)


# ----------------------------
# Footer
# ----------------------------

st.success(
    f"✅ {brand} Premium Analytics Dashboard Loaded Successfully"
)


