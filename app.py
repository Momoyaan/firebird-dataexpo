import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="Coffee Sales Analysis")
with open("styles.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)
    st.markdown(
        """
        <style>
        [data-testid=stSidebar] {
            border-right: 1px solid #39393B !important;}
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("index.csv")
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    df["hour"] = df["datetime"].dt.hour
    df["day"] = df["datetime"].dt.day
    df["month"] = df["datetime"].dt.month
    df["day_name"] = df["datetime"].dt.day_name()
    days_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    df["day_name"] = pd.Categorical(df["day_name"], categories=days_order, ordered=True)
    return df


color_palette = px.colors.qualitative.Light24


def colorize_multiselect_options(colors: list[str]) -> None:
    rules = ""
    n_colors = len(colors)

    for i, color in enumerate(colors):
        rules += f""".stMultiSelect div[data-baseweb="select"] span[data-baseweb="tag"]:nth-child({n_colors}n+{i + 1}){{background-color: {color};}}"""

    st.markdown(f"<style>{rules}</style>", unsafe_allow_html=True)


df = load_data()

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to", ["Overview", "Sales Analysis", "Payment Analysis", "Conclusion"]
)

# Main content
st.title("Midterm Activity: Streamlit Data Exploration App")

if page == "Overview":
    st.write(
        "This dataset contains records of coffee sales transactions from a vending machine. "
        "It includes information about each sale, the type of coffee purchased, mode of payment, "
        "the time of transaction, and other relevant details."
    )
    st.write(
        "The main purpose of this dataset is to help analyze customer purchasing habits, "
        "track sales trends, and discover customer preferences for different coffee products."
    )

    st.divider()

    st.write("### Data Types:")
    st.write(df.dtypes)

    st.divider()

    with st.expander("See Detailed Statistics"):
        numeric_df = df.select_dtypes(include=[np.number])
        if not numeric_df.empty:
            st.write("### Statistics Summary:")
            st.write(numeric_df.describe())

    st.divider()

    st.write("### First 10 Rows of Data")
    st.write(df.head(10))


elif page == "Sales Analysis":
    st.write("## Sales Analysis")

    st.divider()

    # Total Sales by Coffee
    st.write("### Total Sales by Coffee")
    total_sales_by_coffee = (
        df.groupby("coffee_name")["money"].sum().sort_values(ascending=True)
    )
    fig = px.bar(
        x=total_sales_by_coffee.index,
        y=total_sales_by_coffee.values,
        labels={"x": "Coffee Name", "y": "Total Sales"},
        color=total_sales_by_coffee.index,
        color_discrete_sequence=color_palette,
    )

    fig.update_layout(
        xaxis={"categoryorder": "total ascending"},
        showlegend=False,
    )

    st.plotly_chart(fig)

    st.write("### Overview")
    st.write(
        "The bar chart titled Total Sales by Coffee' provides a visual representation of the popularity and sales performance of various coffee types within the vending machine. It allows us to quickly identify the best-selling coffee products and understand customer preferences."
    )

    st.write("    ")
    st.write("### Insights")
    st.markdown("""
    - **Latte Dominates**: The "Latte" stands out as the most popular coffee, significantly outselling all other options. This suggests a strong preference for this classic beverage among customers.
    - **Cappuccino and Americano Follow**: "Cappuccino" and "Americano" occupy the second and third positions, respectively, indicating a consistent demand for these coffee varieties.
    - **Espresso and Cocoa: Niche Favorites**: "Espresso" and "Cocoa" have lower sales compared to the top three, suggesting they cater to a more specific customer segment or preference.
    - **Cortado and Hot Chocolate: Mid-Range Popularity**: "Cortado" and "Hot Chocolate" fall somewhere in between, demonstrating moderate popularity and appeal to a wider range of customers.
    """)
    st.divider()

    # Number of Sales by Coffee
    st.write("### Number of Sales by Coffee")

    # Assuming total_sales_by_coffee is already calculated as before
    sorted_count_sale = (
        df["coffee_name"].value_counts().reindex(total_sales_by_coffee.index)
    )

    colors = px.colors.qualitative.Light24

    fig = go.Figure()

    # Add the line plot
    fig.add_trace(
        go.Scatter(
            x=sorted_count_sale.index,
            y=sorted_count_sale.values,
            mode="lines+markers",
            name="Number of Sales",
            line=dict(color=colors[0], width=3),
            marker=dict(
                size=10, color=colors, line=dict(width=2, color="DarkSlateGrey")
            ),
        )
    )

    # Update layout
    fig.update_layout(
        title="Number of Sales by Coffee",
        xaxis_title="Coffee Name",
        yaxis_title="Number of Sales",
        hovermode="x unified",
        xaxis=dict(tickangle=45),
    )
    # Make the chart responsive
    fig.update_layout(
        autosize=True,
        width=800,
        height=500,
    )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

    st.write("### Overview")
    st.write(
        "The line chart titled 'Number of Sales by Coffee' provides a visual representation of the sales volume for each coffee type within the vending machine. It allows us to compare the popularity of different coffee products and identify any trends or patterns in sales."
    )
    st.write("    ")

    st.write("### Insights")
    st.markdown("""
    - **Latte and Americano with Milk: Consistent Popularity**: Both "Latte" and "Americano with Milk" show relatively high and consistent sales throughout the observed period, indicating a sustained demand for these beverages.
    - **Cappuccino and Cortado: Increasing Popularity**: "Cappuccino" and "Cortado" demonstrate a gradual increase in sales, suggesting that their popularity is growing over time.
    - **Espresso, Cocoa, and Hot Chocolate: Fluctuating Sales**: "Espresso," "Cocoa," and "Hot Chocolate" exhibit more variable sales patterns, with peaks and troughs suggesting that their popularity may be influenced by seasonal factors, promotions, or other external variables.
    """)

    st.divider()

    colorize_multiselect_options(colors)

    selected_coffee = st.multiselect(
        "Select Coffee Types",
        df["coffee_name"].unique(),
        default=df["coffee_name"].unique(),
    )
    filtered_df = df[df["coffee_name"].isin(selected_coffee)]

    # Heatmap
    st.write("### Sales Count by Coffee per Day")
    sale_by_coffee_perday = (
        filtered_df.groupby(["day_name", "coffee_name"])["money"]
        .count()
        .unstack()
        .fillna(0)
    )

    # Create heatmap using Plotly Express
    fig = px.imshow(
        sale_by_coffee_perday,
        text_auto=".0f",
        color_continuous_scale="bluered",
        aspect="auto",
    )
    fig.update_layout(
        title="Sales Count by Coffee per Day",
        xaxis_title="Coffee Name",
        yaxis_title="Day of the Week",
    )

    # Rotate x-axis labels
    fig.update_xaxes(tickangle=40)

    # Display in Streamlit
    st.plotly_chart(fig)

    st.write("### Overview")
    st.write(
        "The line chart titled 'Number of Sales by Coffee' provides a visual representation of the sales volume for each coffee type within the vending machine. It allows us to compare the popularity of different coffee products and identify any trends or patterns in sales."
    )
    st.write("    ")

    st.write("### Insights")
    st.markdown("""
    - **Latte and Americano with Milk: Consistent Popularity**: Both "Latte" and "Americano with Milk" show relatively high and consistent sales throughout the observed period, indicating a sustained demand for these beverages.
    - **Cappuccino and Cortado: Increasing Popularity**: "Cappuccino" and "Cortado" demonstrate a gradual increase in sales, suggesting that their popularity is growing over time.
    - **Espresso, Cocoa, and Hot Chocolate: Fluctuating Sales**: "Espresso," "Cocoa," and "Hot Chocolate" exhibit more variable sales patterns, with peaks and troughs suggesting that their popularity may be influenced by seasonal factors, promotions, or other external variables.
    """)

    st.divider()

    tab1, tab2, tab3 = st.tabs(["Daily Sales", "Monthly Sales", "Coffee Type Analysis"])

    with tab1:
        st.write("### Total Sales by Weekday")
        fig = px.bar(
            df,
            x="day_name",
            y="money",
            color="day_name",
            color_discrete_sequence=px.colors.qualitative.Light24,
        )
        st.plotly_chart(fig)
        st.markdown("""
        ### Overview
        The bar chart titled *"Total Sales by Weekday"* provides a visual representation of the total sales generated for each day of the week. The height of each bar indicates the total sales volume for that particular day.

        ### Insights:
        - **Highest Sales on Tuesday**: Tuesday emerges as the day with the highest total sales, significantly outperforming the other days of the week.
        - **Consistent Sales on Weekdays**: Monday, Thursday, Friday, and Saturday exhibit relatively consistent sales levels, suggesting a steady demand for coffee during these days.
        - **Lower Sales on Weekends**: Sunday and Wednesday generally have lower total sales compared to the other weekdays. This might indicate a decrease in customer activity or a shift in purchasing patterns during these days.
        """)

    with tab2:
        st.write("### Total Sales by Month")
        df["month_name"] = df["datetime"].dt.strftime("%B")
        fig = px.bar(
            df,
            x="month_name",
            y="money",
            color="month_name",
            color_discrete_sequence=px.colors.qualitative.Light24,
        )
        st.plotly_chart(fig)
        st.markdown("""
        ### Overview
        The bar chart titled *"Total Sales by Month"* provides a visual representation of the total sales generated for each month. The height of each bar indicates the total sales volume for that particular month.

        ### Insights:
        - **Highest Sales in September**: September emerges as the month with the highest total sales, significantly outperforming the other months.
        - **Consistent Sales Throughout the Year**: The overall sales volume appears relatively consistent throughout the year, with minor fluctuations between months.
        - **Slight Dip in July**: July shows a slight dip in sales compared to the surrounding months.
        """)

    with tab3:
        st.write("### Preferred Coffee Each Month")
        monthly_coffee_sales = (
            df.groupby(["month", "coffee_name"])["money"].sum().reset_index()
        )
        fig = px.bar(
            monthly_coffee_sales,
            x="month",
            y="money",
            color="coffee_name",
            color_discrete_sequence=px.colors.qualitative.Light24,
        )
        st.plotly_chart(fig)
        st.markdown("""
        ### Overview

        The bar chart titled "Preferred Coffee Type Each Month" provides a visual representation of the sales volume for each coffee type across different months. The height of each bar indicates the total sales for that particular coffee type in the corresponding month.

        ### Key Insights:

        - **Latte Dominance**: "Latte" consistently has the highest sales volume across all months, indicating a strong preference for this coffee type.
        - **Seasonal Variations**: There are noticeable seasonal variations in the sales of "Cappuccino" and "Americano with Milk." "Cappuccino" tends to have higher sales in the earlier months (March - May), while "Americano with Milk" has higher sales in the later months (July - September).
        - **Consistent Sales for Americano with Milk**: "Americano with Milk" maintains relatively consistent sales throughout the year, suggesting a steady demand for this coffee type.
        """)


elif page == "Payment Analysis":
    st.write("## Payment Analysis")

    # Total Sales by Payment Type
    st.write("### Total Sales by Payment Type")
    total_sales_by_payment = df.groupby("cash_type")["money"].sum()
    fig = px.pie(
        values=total_sales_by_payment.values,
        names=total_sales_by_payment.index,
        color_discrete_sequence=px.colors.qualitative.Light24,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig)

    # Number of Sales by Payment Type
    st.write("### Number of Sales by Payment Type")
    number_of_sales_by_payment = df["cash_type"].value_counts()
    fig = px.pie(
        values=number_of_sales_by_payment.values,
        names=number_of_sales_by_payment.index,
        color_discrete_sequence=px.colors.qualitative.Light24,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig)

    st.write("### Distribution of Cash Type")
    cash_type_distribution = (
        df["cash_type"].value_counts().sort_values(ascending=True).reset_index()
    )
    cash_type_distribution.columns = ["cash_type", "count"]
    fig = px.bar(
        cash_type_distribution,
        x="cash_type",
        y="count",
        color="cash_type",
        color_discrete_map={"cash": "#00FE35", "card": "#FD3216"},
    )
    fig.update_traces(texttemplate="%{y}", textposition="outside")
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    ### Overview

    These charts provide insights into the payment methods used by customers and their impact on sales.

    ### Total Sales by Payment Type
    - **Dominance of Card Payments**: 94.2% of total sales are made using cards, indicating a strong preference for card payments.
    - **Cash Payments**: Cash payments account for only 5.8% of total sales.

    ### Number of Sales by Payment Type
    - **Similar Distribution**: The distribution of sales by payment type is similar to the total sales distribution, with cards being the predominant method.
    - **Slight Difference**: Cash payments account for a slightly higher proportion of total sales (5.1%) compared to the number of sales, suggesting that cash transactions might involve larger amounts on average.
    """)

else:  # Conclusion
    st.write("# Conclusion")
    st.write(
        "The analysis of coffee sales reveals significant insights on customer behavior and their preferences. "
        "'Latte' consistently emerges as the top-selling coffee, showing a strong demand for this beverage throughout the year."
    )
    st.write(
        "These insights imply that coffee businesses should prioritize stocking coffees like 'Latte', "
        "followed by 'Americano with Milk', and 'Cappuccino'. Further analysis could investigate the impact of "
        "marketing strategies on sales and explore customer preferences of coffee types."
    )

# Add a date range selector
start_date, end_date = st.sidebar.date_input(
    "Select Date Range", [df["datetime"].min().date(), df["datetime"].max().date()]
)
filtered_df = df[
    (df["datetime"].dt.date >= start_date) & (df["datetime"].dt.date <= end_date)
]


# Download data
@st.cache_data
def convert_df(df):
    return df.to_csv().encode("utf-8")


csv = convert_df(filtered_df)
st.sidebar.download_button(
    label="Download data as CSV",
    data=csv,
    file_name="coffee_sales_data.csv",
    mime="text/csv",
)
