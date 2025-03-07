# ----------------------------
# Import Libraries
# ----------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime
import streamlit as st

# ----------------------------
# Load and Preprocess Data
# ----------------------------
# Load dataset
day_df = pd.read_csv("https://raw.githubusercontent.com/echaan/bike-sharing-analysis/refs/heads/main/data/day.csv")

# Remove irrelevant columns
drop_columns = ['instant', 'windspeed']
day_df.drop(columns=drop_columns, inplace=True)

# Rename columns for clarity
day_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'cnt': 'count'
}, inplace=True)

# Convert 'dateday' to datetime
day_df['dateday'] = pd.to_datetime(day_df['dateday'])

# Add additional date-related columns
day_df['weekday'] = day_df['dateday'].dt.day_name()
day_df['year'] = day_df['dateday'].dt.year

# Map numerical values to categorical labels
day_df['season'] = day_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})

day_df['weathersit'] = day_df['weathersit'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})

# Resample data by month
monthly_df = day_df.resample(rule='M', on='dateday').agg({
    "casual": "sum",
    "registered": "sum",
    "count": "sum"
})
monthly_df.index = monthly_df.index.strftime('%b-%y')
monthly_df = monthly_df.reset_index()
monthly_df.rename(columns={
    "dateday": "yearmonth",
    "count": "total_rides",
    "casual": "casual_rides",
    "registered": "registered_rides"
}, inplace=True)

# Fungsi untuk melakukan groupby dan agregasi
def calculate_stats(df, group_col, agg_col, agg_funcs):
    return df.groupby(group_col)[agg_col].agg(agg_funcs)

# Agregasi untuk berbagai kelompok data
month_stats = calculate_stats(day_df, 'month', 'count', ['max', 'min', 'mean', 'sum'])
weather_stats = calculate_stats(day_df, 'weathersit', 'count', ['max', 'min', 'mean', 'sum'])
holiday_stats = calculate_stats(day_df, 'holiday', 'count', ['max', 'min', 'mean', 'sum'])
weekday_stats = calculate_stats(day_df, 'weekday', 'count', ['max', 'min', 'mean'])
workingday_stats = calculate_stats(day_df, 'workingday', 'count', ['max', 'min', 'mean'])

# Agregasi untuk season dengan kolom yang berbeda
season_stats = day_df.groupby('season').agg({
    'casual': 'mean',
    'registered': 'mean',
    'count': ['max', 'min', 'mean']
})

# Agregasi untuk variabel cuaca berdasarkan season
season_weather_stats = day_df.groupby('season').agg({
    'temp': ['max', 'min', 'mean'],
    'atemp': ['max', 'min', 'mean'],
    'hum': ['max', 'min', 'mean']
})

# ----------------------------
# Streamlit Sidebar
# ----------------------------
with st.sidebar:
    # Sidebar logo
    st.image("https://cdn-icons-png.flaticon.com/512/2972/2972185.png")  # Ikon sepeda

    # Date filter
    st.header("Pilih Rentang Tanggal")
    min_date = day_df["dateday"].min()
    max_date = day_df["dateday"].max()
    start_date, end_date = st.date_input(
        label="Pilih Tanggal Mulai dan Tanggal Akhir",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
        help="Pilih rentang tanggal untuk menampilkan data yang sesuai."
    )

    st.header("About This Dashboard")

    # Informasi Tambahan
    st.markdown("""
        This dashboard provides insights into bike sharing trends and usage patterns.
        - **Data Source**: [Bike Sharing Dataset](https://drive.google.com/file/d/1RaBmV6Q6FYWU4HWZs80Suqd7KQC34diQ/view?usp=sharing)
        - **Last Updated**: March 2025
        - **Contact**: [akkitherythm@gmail.com](mailto:akkitherythm@gmail.com)
    """)

    st.markdown("---")
    st.markdown("**Connect with Me**")
    st.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-Eric_Chaniago-blue?style=flat&logo=linkedin)](https://id.linkedin.com/in/m-eric-chaniago-994684232?trk=public_profile_browsemap)")

    # Dataset link
    st.markdown("**Github Project:** [Repository](https://github.com/echaan/bike-sharing-analysis)")
# ---------------------------------------------------------------------------------

# Filter main dataframe based on selected date range
main_df = day_df[
    (day_df["dateday"] >= str(start_date)) &
    (day_df["dateday"] <= str(end_date))
]

# ----------------------------
# Streamlit Main Page
# ----------------------------
# Title
st.title("Bike Sharing Dashboard")
tab1, tab2, tab3 = st.tabs(["Overview", "Trends", "Analysis"])

with tab1:
    # Header dan Deskripsi
    st.markdown("""
        ### **Overview** 🚴‍♂️
        Welcome to the **Bike Sharing Dashboard**! This dashboard provides a quick yet comprehensive overview of bike sharing data, helping you understand key trends and patterns. Whether you're a city planner, a bike sharing operator, or a data enthusiast, this tool is designed to give you actionable insights to optimize bike sharing systems.
    """)

    # Metrics
      # Metrics
    st.markdown("### **Key Metrics** 📊")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Rides", value=f"{main_df['count'].sum():,}")
    with col2:
        st.metric("Total Casual Rides", value=f"{main_df['casual'].sum():,}")
    with col3:
        st.metric("Total Registered Rides", value=f"{main_df['registered'].sum():,}")
    st.markdown("---")

    # Seasonal Usage
    st.markdown("### **Seasonal Usage** 🌸☀️🍂❄️")
    st.markdown("""
        Explore how bike rentals vary across different seasons. The chart below shows the total number of rides by **casual** and **registered** users for each season.
    """)
    seasonal_usage = day_df.groupby('season')[['registered', 'casual']].sum().reset_index()
    fig = px.bar(seasonal_usage, x='season', y=['registered', 'casual'],
                 title='Bike Rental Counts by Season',
                 barmode='group',
                 labels={'value': 'Total Rides', 'variable': 'User Type'},
                 color_discrete_sequence=["#1f77b4", "#ff7f0e"])  # Warna yang lebih menarik
    st.plotly_chart(fig, use_container_width=True)

    # Penjelasan Grafik dengan Expander
    with st.expander("📝 **Insights: What does this chart tell us?**"):
        st.markdown("""
            - The highest number of bike rentals occurs in **Fall**, followed by **Summer** and **Winter**, while **Spring** has the lowest number of rentals.
            - This indicates that **Fall** and **Summer** are more conducive for biking activities, likely due to pleasant weather conditions.
            - **Spring**, which tends to be wetter or colder, may reduce the interest in bike rentals.
        """)

with tab2:
    st.markdown("""
        ### **Trends**
        Explore usage trends over time.
    """)

    # Monthly Rentals
    st.markdown("### **Monthly Rentals**")
    monthly_df['total_rides'] = monthly_df['casual_rides'] + monthly_df['registered_rides']
    fig = px.bar(monthly_df,
                 x='yearmonth',
                 y=['casual_rides', 'registered_rides', 'total_rides'],
                 barmode='group',
                 title="Bike Rental Trends in Recent Years",
                 labels={'casual_rides': 'Casual Rentals', 'registered_rides': 'Registered Rentals', 'total_rides': 'Total Rides'})
    st.plotly_chart(fig, use_container_width=True)

    # Insights with Expander
    with st.expander("📝 **Insights: What does this chart tell us?**"):
        st.markdown("""
            - **Consistent Growth**: Bike rentals in 2012 are consistently higher than in 2011 across all months.
            - **Significant Increase**: A notable increase is observed from March to September, with the peak occurring in September.
            - **Trend Analysis**: This indicates a growing trend in bike usage year over year, likely influenced by factors such as favorable weather conditions or increased public interest in cycling.
        """)

    # Scatter Plot: Season vs Temperature
    st.markdown("### **Season vs Temperature**")
    fig = px.scatter(day_df, x='temp', y='count', color='season',
                     title='Bike Rental Clusters by Season and Temperature',
                     labels={'temp': 'Temperature (°C)', 'count': 'Total Rides'})
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown("""
        ### **Analysis**
        Dive deep into user behavior and seasonal patterns.
    """)

    # Weather Distribution
    st.markdown("### **Weather Distribution**")
    fig = px.box(day_df, x='weathersit', y='count', color='weathersit',
                 title='Bike Users Distribution Based on Weather Condition',
                 labels={'weathersit': 'Weather Condition', 'count': 'Total Rides'})
    st.plotly_chart(fig, use_container_width=True)

    # Working Day, Holiday, and Weekday Analysis
    st.markdown("### **Working Day, Holiday, and Weekday Analysis**")

    # Working Day vs Holiday
    st.markdown("#### **Working Day vs Holiday**")
    workingday_usage = day_df.groupby('workingday')['count'].sum().reset_index()
    workingday_usage['workingday'] = workingday_usage['workingday'].map({0: 'Holiday/Weekend', 1: 'Working Day'})
    fig1 = px.bar(workingday_usage, x='workingday', y='count',
                  title='Total Bike Rentals: Working Day vs Holiday/Weekend',
                  labels={'workingday': 'Day Type', 'count': 'Total Rides'},
                  color='workingday',
                  color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig1, use_container_width=True)

    # Weekday Analysis
    st.markdown("#### **Weekday Analysis**")
    weekday_usage = day_df.groupby('weekday')['count'].sum().reset_index()
    fig2 = px.bar(weekday_usage, x='weekday', y='count',
                  title='Total Bike Rentals by Weekday',
                  labels={'weekday': 'Weekday', 'count': 'Total Rides'},
                  color='weekday',
                  color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig2, use_container_width=True)
# Footer
st.caption('Copyright (c), created by echaan')