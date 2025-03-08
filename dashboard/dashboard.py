# ----------------------------
# Import Libraries
# ----------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

# Function to perform groupby and aggregation
def calculate_stats(df, group_col, agg_col, agg_funcs):
    return df.groupby(group_col)[agg_col].agg(agg_funcs)

# Aggregation for various data groups
month_stats = calculate_stats(day_df, 'month', 'count', ['max', 'min', 'mean', 'sum'])
weather_stats = calculate_stats(day_df, 'weathersit', 'count', ['max', 'min', 'mean', 'sum'])
holiday_stats = calculate_stats(day_df, 'holiday', 'count', ['max', 'min', 'mean', 'sum'])
weekday_stats = calculate_stats(day_df, 'weekday', 'count', ['max', 'min', 'mean'])
workingday_stats = calculate_stats(day_df, 'workingday', 'count', ['max', 'min', 'mean'])

# Aggregation for season with different columns
season_stats = day_df.groupby('season').agg({
    'casual': 'mean',
    'registered': 'mean',
    'count': ['max', 'min', 'mean']
})

# Aggregation for weather variables by season
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
    st.image("https://cdn-icons-png.flaticon.com/512/2972/2972185.png")  # Bike icon

    # Date filter
    st.header("Select Date Range")
    min_date = day_df["dateday"].min()
    max_date = day_df["dateday"].max()
    start_date, end_date = st.date_input(
        label="Select Start and End Date",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
        help="Select a date range to display relevant data."
    )

    st.header("About This Dashboard")

    # Additional Information
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
    # Header and Description
    st.markdown("""
        ### **Overview** 🚴‍♂️
        Welcome to the **Bike Sharing Dashboard**! This dashboard provides a quick yet comprehensive overview of bike sharing data, helping you understand key trends and patterns. Whether you're a city planner, a bike sharing operator, or a data enthusiast, this tool is designed to give you actionable insights to optimize bike sharing systems.
    """)

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

with tab2:
    st.markdown("""
        ### **Trends**
        Explore usage trends over time.
    """)

    # Monthly Rentals
    st.markdown("### **Monthly Rentals**")

    # Create data for line chart
    monthly_counts = day_df.groupby(['month', 'year'])['count'].sum().reset_index()

    # Map month numbers to month names
    month_names = [
        'January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    monthly_counts['month'] = monthly_counts['month'].map(lambda x: month_names[x - 1])

    # Plot line chart
    plt.figure(figsize=(10, 5), facecolor='none')  # Transparent canvas
    ax = sns.lineplot(
        data=monthly_counts,
        x="month",
        y="count",
        hue="year",
        marker="o",
        palette="Set2"
    )

    # Add title and labels
    plt.title("Total Bike Rentals by Month and Year", fontsize=14, color='#666666')  # Grey title
    plt.xlabel(None)
    plt.ylabel(None)
    plt.xticks(rotation=45, color='#666666')  # Rotate month labels and set text color
    plt.yticks(color='#666666')  # Set y-axis text color

    # Set plot background to transparent
    ax.set_facecolor('none')  # Transparent plot background

    # Set axis line colors
    ax.spines['bottom'].set_color('#CCCCCC')  # Light grey x-axis line
    ax.spines['left'].set_color('#CCCCCC')  # Light grey y-axis line

    # Set legend
    plt.legend(title="Year", loc="upper right", title_fontsize=12, fontsize=10, facecolor='#666666', edgecolor='none')

    # Display plot in Streamlit
    st.pyplot(plt)

    # Insights with Expander
    with st.expander("📝 **Insights: What does this chart tell us?**"):
        st.markdown("""
            - **Consistent Growth**: Bike rentals in 2012 are consistently higher than in 2011 across all months.
            - **Significant Increase**: A notable increase is observed from March to September, with the peak occurring in September.
            - **Trend Analysis**: This indicates a growing trend in bike usage year over year, likely influenced by factors such as favorable weather conditions or increased public interest in cycling.
        """)

with tab3:
    st.markdown("""
        ### **Analysis**
        Dive deep into user behavior and seasonal patterns.
    """)

    # Weather Distribution
    st.markdown("### **Weather Distribution**")

    # Mapping weather categories
    weather_mapping = {
        1: "Clear/Partly Cloudy",
        2: "Misty/Cloudy",
        3: "Light Snow/Rain",
        4: "Heavy Rain/Snow"
    }

    # Set figure size and transparent canvas
    plt.figure(figsize=(10, 6), facecolor='none')

    # Custom color palette
    custom_palette = ["#F37199", "#AC1754", "#F7A8C4", "#E53888"]

    # Create barplot for bike rentals by weather condition
    ax = sns.barplot(data=day_df, x='weathersit', y='count', palette=custom_palette)

    # Add title and axis labels
    plt.title('Bike Rentals Distribution by Weather Condition', fontsize=14, color='#666666')  # Grey title
    plt.xlabel(None)
    plt.ylabel('Total Bike Rentals', fontsize=12, color='#666666')  # Grey y-axis label

    # Set axis text colors
    plt.xticks(color='#666666')  # Grey x-axis text
    plt.yticks(color='#666666')  # Grey y-axis text

    # Set plot background to transparent
    ax.set_facecolor('none')  # Transparent plot background

    # Set axis line colors
    ax.spines['bottom'].set_color('#CCCCCC')  # Light grey x-axis line
    ax.spines['left'].set_color('#CCCCCC')  # Light grey y-axis line

    # Display plot in Streamlit
    st.pyplot(plt)

    # Insights with Expander
    with st.expander("📝 **Insights: What does this chart tell us?**"):
        st.markdown("""
            - **Clear/Partly Cloudy**: The highest number of bike rentals occurs in clear or partly cloudy weather, indicating that sunny weather is highly conducive to biking.
            - **Misty/Cloudy**: Bike rentals decrease slightly in misty or cloudy weather, but it remains a popular choice for riders.
            - **Light Snow/Rain**: Bike rentals drop significantly during light snow or rain, as these conditions make cycling less comfortable.
            - **Heavy Rain/Snow**: The lowest number of bike rentals occurs during heavy rain or snow, as these conditions are least favorable for cycling.
        """)

    # Seasonal Usage
    st.markdown("### **Seasonal Usage** 🌸☀️🍂❄️")
    st.markdown("""
        Explore how bike rentals vary across different seasons. The chart below shows the total number of rides for each season.
    """)

    # Create visualization for bike rentals by season
    plt.figure(figsize=(10, 6), facecolor='none')  # Transparent canvas
    custom_palette = ["#F37199", "#E53888", "#AC1754", "#F7A8C4"] 
    ax = sns.barplot(data=day_df, x='season', y='count', palette=custom_palette, estimator=sum, ci=None)

    # Add title and axis labels
    plt.title('Total Bike Rentals by Season', fontsize=14, color='#E53888')  
    plt.xlabel('Season', fontsize=12, color='#E53888')  
    plt.ylabel('Total Bike Rentals', fontsize=12, color='#E53888') 

    # Set plot background and axis line colors
    ax.set_facecolor('none')  # Transparent plot background
    plt.gca().spines['bottom'].set_color('#CCCCCC')  
    plt.gca().spines['left'].set_color('#CCCCCC')  
    plt.gca().tick_params(axis='x', colors='#666666')  # Grey x-axis text
    plt.gca().tick_params(axis='y', colors='#666666')  # Grey y-axis text

    # Display plot in Streamlit
    st.pyplot(plt)

    # Insights with Expander
    with st.expander("📝 **Insights: What does this chart tell us?**"):
        st.markdown("""
            - The highest number of bike rentals occurs in **Fall**, followed by **Summer** and **Winter**, while **Spring** has the lowest number of rentals.
            - This indicates that **Fall** and **Summer** are more conducive for biking activities, likely due to pleasant weather conditions.
            - **Spring**, which tends to be wetter or colder, may reduce the interest in bike rentals.
        """)
    
# Footer
st.caption('Copyright (c), created by echaan')