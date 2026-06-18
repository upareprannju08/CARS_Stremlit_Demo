import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os


# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(
    page_title="Premium Car Dashboard",
    page_icon="🚘",
    layout="wide"
)


# -------------------------
# Custom Dark Theme
# -------------------------
st.markdown("""
<style>

.stApp{
    background: #050816;
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background: linear-gradient(180deg,#000000,#001f3f);
}

/* Headings */
h1,h2,h3{
    color:#00BFFF;
    text-align:center;
    font-weight:bold;
}

/* Metrics */
[data-testid="stMetric"]{
    background:#071425;
    border:1px solid #00BFFF;
    padding:15px;
    border-radius:15px;
    box-shadow:0 0 12px #00BFFF;
}

/* Select Box */
.stSelectbox label{
    color:white !important;
}

</style>
""", unsafe_allow_html=True)


# -------------------------
# Load Dataset
# -------------------------
df = pd.read_csv("CARS.csv")


# Clean price columns
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


# -------------------------
# Sidebar Filters
# -------------------------
st.sidebar.title("🔎 Filter Cars")


brand_list = sorted(df["Make"].unique())

brand = st.sidebar.selectbox(
    "Select Brand",
    brand_list
)


brand_df = df[df["Make"] == brand]


types = sorted(brand_df["Type"].unique())

car_type = st.sidebar.selectbox(
    "Select Type",
    types
)


filtered = brand_df[brand_df["Type"] == car_type]


# -------------------------
# Brand Logo Section
# -------------------------

logo_path = f"logos/{brand}.png"


col1, col2 = st.columns([1, 5])


with col1:
    if os.path.exists(logo_path):
        st.image(
            logo_path,
            width=130
        )


with col2:
    st.markdown(
        f"""
        <h1>{brand} Analytics Dashboard</h1>
        """,
        unsafe_allow_html=True
    )


# -------------------------
# Dashboard Metrics
# -------------------------

m1, m2, m3, m4 = st.columns(4)


m1.metric(
    "🚗 Total Cars",
    len(df)
)

m2.metric(
    "🏢 Brands",
    df["Make"].nunique()
)


m3.metric(
    "⚙ Avg Horsepower",
    int(df["Horsepower"].mean())
)


m4.metric(
    "💰 Max Price",
    f"${df['MSRP'].max():,}"
)


plt.style.use("dark_background")


# =========================
# SECTION 1
# =========================

st.header("📊 Brand Performance")


c1, c2 = st.columns(2)


with c1:

    fig, ax = plt.subplots(figsize=(8,5))

    sns.barplot(
        data=filtered,
        x="Model",
        y="MPG_City",
        palette="Blues",
        ax=ax
    )

    ax.set_title("City MPG by Model")
    plt.xticks(rotation=90)

    st.pyplot(fig)


with c2:

    fig, ax = plt.subplots(figsize=(8,5))

    sns.scatterplot(
        data=df,
        x="Horsepower",
        y="EngineSize",
        hue="Origin",
        ax=ax
    )

    ax.set_title("Horsepower vs Engine Size")

    st.pyplot(fig)


# =========================
# SECTION 2
# =========================

st.header("📈 Market Insights")


c3, c4 = st.columns(2)


with c3:

    fig, ax = plt.subplots()

    sns.countplot(
        data=df,
        x="Type",
        palette="Blues",
        ax=ax
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

    ax.set_title("Car Origin Distribution")

    st.pyplot(fig)



with c4:

    fig, ax = plt.subplots()

    sns.barplot(
        data=df,
        x="DriveTrain",
        y="MSRP",
        palette="winter",
        ax=ax
    )

    ax.set_title("Price by Drive Train")

    st.pyplot(fig)


    fig, ax = plt.subplots()

    sns.pointplot(
        data=df,
        x="DriveTrain",
        y="Horsepower",
        color="cyan",
        ax=ax
    )

    ax.set_title(
        "Horsepower by DriveTrain"
    )

    st.pyplot(fig)


# =========================
# SECTION 3
# =========================

st.header("🔥 Correlation Heatmap")


fig, ax = plt.subplots(
    figsize=(12,6)
)


sns.heatmap(
    df.corr(numeric_only=True),
    annot=True,
    cmap="Blues",
    ax=ax
)


st.pyplot(fig)


# Footer
st.success(
    "✅ Premium Car Analytics Dashboard Loaded Successfully"
)


