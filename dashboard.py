import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.title
st.write


st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

def create_monthly_rent_df(df):
    monthly_rent_df = df.resample(rule='M', on='dteday').agg({
        "cnt": "sum",
        "registered": "sum",
        "casual": "sum"
    }).reset_index()
    monthly_rent_df.rename(columns={"cnt": "total_rentals"}, inplace=True)
    return monthly_rent_df

def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by="weathersit").agg({
        "cnt": "mean"
    }).reset_index()
    return weather_rent_df

all_df = pd.read_csv("day.csv")
all_df['dteday'] = pd.to_datetime(all_df['dteday'])
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png") # Opsional: Logo
    
    min_date = all_df["dteday"].min()
    max_date = all_df["dteday"].max()
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

monthly_df = create_monthly_rent_df(main_df)
weather_df = create_weather_rent_df(main_df)

st.header('🚲 Bike Sharing Dashboard')

col1, col2, col3 = st.columns(3)
with col1:
    total_rentals = main_df.cnt.sum()
    st.metric("Total Rentals", value=f"{total_rentals:,}")

with col2:
    total_registered = main_df.registered.sum()
    st.metric("Total Registered", value=f"{total_registered:,}")

with col3:
    total_casual = main_df.casual.sum()
    st.metric("Total Casual", value=f"{total_casual:,}")

st.markdown("---")

st.subheader('Monthly Rentals Trend')
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_df["dteday"],
    monthly_df["total_rentals"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Rentals by Weather Condition")
    weather_df['weathersit'] = weather_df['weathersit'].map({
        1: 'Clear', 2: 'Misty', 3: 'Light Rain/Snow', 4: 'Heavy Rain'
    })
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x="weathersit", 
        y="cnt", 
        data=weather_df, 
        palette="viridis",
        ax=ax
    )
    ax.set_title("Average Rentals by Weather", fontsize=15)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    st.pyplot(fig)

with col2:
    st.subheader("User Contribution Ratio")
    labels = ['Casual', 'Registered']
    sizes = [main_df['casual'].sum(), main_df['registered'].sum()]
    colors = ['#FF9999', '#66B3FF']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, explode=(0.1, 0))
    ax.axis('equal') 
    st.pyplot(fig)

st.caption('Copyright (c) 2026 - Bike Sharing Project Analysis')
