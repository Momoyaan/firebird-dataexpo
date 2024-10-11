import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


df = pd.read_csv('index.csv')

st.title("Midterm Activity: Streamlit Data Exploration App")
st.divider()

st.write("This dataset contains records of coffee sales transactions from a vending machine. This includes information about each sale, the type of coffee purchased, mode of payment, the time of transaction, and other relevant details. This dataset aims to provide valuable data for the community to explore. The dataset spans from March to September 2024")
st.write("The main purpose of this dataset is to help analyze customer purchasing habits, track sales trends, and discover customer’s preferences for different coffee products. This dataset helps us gain insights such as peak sales periods, and which coffee types are most popular.")
st.divider()
st.write("### Data Types:")
st.write(df.dtypes)

st.divider()
numeric_df = df.select_dtypes(include=[np.number])

if not numeric_df.empty:
    mean = numeric_df.mean()
    median = numeric_df.median()
    mode = numeric_df.mode().iloc[0]
    std_dev = numeric_df.std()
    variance = numeric_df.var()
    min_values = numeric_df.min()
    max_values = numeric_df.max()
    range_values = max_values - min_values
    percentiles = numeric_df.quantile([0.25, 0.5, 0.75])



    st.write("### Statistics Summary:")
    st.write(f"**Mean:**\n{mean}")
    st.write(f"**Median:**\n{median}")
    st.write(f"**Mode:**\n{mode}")
    st.write(f"**Standard Deviation:**\n{std_dev}")
    st.write(f"**Variance:**\n{variance}")
    st.write(f"**Minimum:**\n{min_values}")
    st.write(f"**Maximum:**\n{max_values}")
    st.write(f"**Range:**\n{range_values}")
    st.write(f"**Percentiles:**\n{percentiles}")

st.divider()
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
df['hour'] = df['datetime'].dt.hour
df['day'] = df['datetime'].dt.day
df['month'] = df['datetime'].dt.month
df['day_name'] = df['datetime'].dt.day_name()
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df['day_name'] = pd.Categorical(df['day_name'], categories=days_order, ordered=True)


st.write("### First 10 Rows of Data")
st.write(df.head(10))
st.divider()

coffee_names = df['coffee_name'].unique()
total_sale_by_coffee = df.groupby('coffee_name')['money'].sum()
count_sale_by_coffee = df.groupby('coffee_name')['money'].count()

sorted_total_sale = total_sale_by_coffee.sort_values()
sorted_count_sale = count_sale_by_coffee.loc[sorted_total_sale.index]

st.write("# Visualization")

st.write("### Total Sales by Coffee")
# Total Sales by Coffee Bar graph
fig, ax1 = plt.subplots(figsize=(12, 8))
color = 'tab:blue'
ax1.set_xlabel('Coffee Name')
ax1.set_ylabel('Total Sales')
ax1.bar(sorted_total_sale.index, sorted_total_sale, color=color, alpha=0.6, label='Total Sales')
ax1.tick_params(axis='y', labelcolor=color)
plt.title('Total Sales by Coffee')
ax1.legend(loc='upper left')
st.pyplot(fig)

st.write("### Overview")
st.write("The bar chart titled Total Sales by Coffee' provides a visual representation of the popularity and sales performance of various coffee types within the vending machine. It allows us to quickly identify the best-selling coffee products and understand customer preferences.")

st.write("    ")
st.write("### Insights")
st.markdown("""
- **Latte Dominates**: The "Latte" stands out as the most popular coffee, significantly outselling all other options. This suggests a strong preference for this classic beverage among customers.
- **Cappuccino and Americano Follow**: "Cappuccino" and "Americano" occupy the second and third positions, respectively, indicating a consistent demand for these coffee varieties.
- **Espresso and Cocoa: Niche Favorites**: "Espresso" and "Cocoa" have lower sales compared to the top three, suggesting they cater to a more specific customer segment or preference.
- **Cortado and Hot Chocolate: Mid-Range Popularity**: "Cortado" and "Hot Chocolate" fall somewhere in between, demonstrating moderate popularity and appeal to a wider range of customers.
""")
st.divider()


# Number of Sales by Coffee Line Graph
st.write("### Number of Sales by Coffee")
fig, ax1 = plt.subplots(figsize=(12, 8))
ax2 = ax1.twinx()
color = 'tab:orange'
ax2.set_ylabel('Number of Sales', color=color)
ax2.plot(sorted_count_sale.index, sorted_count_sale, color=color, marker='o', label='Number of Sales')
ax2.tick_params(axis='y', labelcolor=color)
plt.title('Number of Sales by Coffee')
ax2.legend(loc='upper left')
st.pyplot(fig)

st.write("### Overview")
st.write("The line chart titled 'Number of Sales by Coffee' provides a visual representation of the sales volume for each coffee type within the vending machine. It allows us to compare the popularity of different coffee products and identify any trends or patterns in sales.")
st.write("    ")

st.write("### Insights")
st.markdown("""
- **Latte and Americano with Milk: Consistent Popularity**: Both "Latte" and "Americano with Milk" show relatively high and consistent sales throughout the observed period, indicating a sustained demand for these beverages.
- **Cappuccino and Cortado: Increasing Popularity**: "Cappuccino" and "Cortado" demonstrate a gradual increase in sales, suggesting that their popularity is growing over time.
- **Espresso, Cocoa, and Hot Chocolate: Fluctuating Sales**: "Espresso," "Cocoa," and "Hot Chocolate" exhibit more variable sales patterns, with peaks and troughs suggesting that their popularity may be influenced by seasonal factors, promotions, or other external variables.
""")

st.divider()

# Sales Count by Coffee per Day HEATMAP
st.write("### Sales Count by Coffee per Day")
sale_by_coffee_perday = df.groupby(['day_name', 'coffee_name'])['money'].count().unstack().fillna(0)
fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(sale_by_coffee_perday, cmap='coolwarm', annot=True, fmt='.0f', cbar_kws={'label': 'Number of Sales'}, ax=ax)
ax.set_title('Sales Count by Coffee per Day')
ax.set_xlabel('Coffee Name')
ax.set_xticklabels(ax.get_xticklabels(), rotation=40)
ax.set_ylabel('Day of the Week')
st.pyplot(fig)  

st.markdown("""
### Overview
The heatmap provides a visual representation of the number of sales for each coffee type on different days of the week. The color intensity of each cell indicates the sales volume, with warmer colors representing higher sales and cooler colors representing lower sales.

### Insights:
- **Weekday Patterns**: The heatmap reveals distinct patterns in sales based on the day of the week. For example, *Latte* consistently has high sales on weekdays, while *Espresso* and *Cocoa* tend to have higher sales on weekends.
- **Peak Sales Days**: Certain coffee types, such as *Cappuccino* and *Americano with Milk*, have peak sales on specific days of the week (e.g., Tuesday and Wednesday).
""")

st.divider()

# Total Sales by Weekday
def plot_sales_by_weekday():
    plt.figure(figsize=(8,6))
    ax = sns.barplot(data=df, x='day_name', y='money', estimator=sum, errorbar=None, 
                     order=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'], 
                     palette="Set2")

    
    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.0f'), 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points')

    
    plt.yticks(range(0, 6001, 1000))
    plt.title("Total Sales by Weekday")
    plt.xlabel('Weekday')
    plt.ylabel("Total Sales")

    plt.tight_layout()
    st.pyplot(plt) 


st.write("### Total Sales by Weekday")


plot_sales_by_weekday()

st.markdown("""
### Overview
The bar chart titled *"Total Sales by Weekday"* provides a visual representation of the total sales generated for each day of the week. The height of each bar indicates the total sales volume for that particular day.

### Insights:
- **Highest Sales on Tuesday**: Tuesday emerges as the day with the highest total sales, significantly outperforming the other days of the week.
- **Consistent Sales on Weekdays**: Monday, Thursday, Friday, and Saturday exhibit relatively consistent sales levels, suggesting a steady demand for coffee during these days.
- **Lower Sales on Weekends**: Sunday and Wednesday generally have lower total sales compared to the other weekdays. This might indicate a decrease in customer activity or a shift in purchasing patterns during these days.
""")

st.divider()


# Total Sales by month
month_mapping = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December"
}


df['month_name'] = df['month'].map(month_mapping)

st.write("### Total Sales by Month")
plt.figure(figsize=(12, 8))
ax = sns.barplot(data=df, x='month_name', y='money', estimator=sum, errorbar=None, palette="Set2")

for p in ax.patches:
    ax.annotate(format(p.get_height(), '.0f'), (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', xytext=(0, 10), textcoords='offset points')

plt.yticks(range(0, 10001, 1000))
plt.title("Total Sales by Month")
plt.xlabel('Months')
plt.ylabel("Total Sales")
plt.xticks(rotation=0) 
plt.tight_layout()

st.pyplot(plt)

st.divider()

st.markdown("""
### Overview
The bar chart titled *"Total Sales by Month"* provides a visual representation of the total sales generated for each month. The height of each bar indicates the total sales volume for that particular month.

### Insights:
- **Highest Sales in September**: September emerges as the month with the highest total sales, significantly outperforming the other months.
- **Consistent Sales Throughout the Year**: The overall sales volume appears relatively consistent throughout the year, with minor fluctuations between months.
- **Slight Dip in July**: July shows a slight dip in sales compared to the surrounding months.
""")

st.divider()

monthly_coffee_sales = df.groupby(['month', 'coffee_name'])['money'].sum().reset_index()


monthly_coffee_sales['month_name'] = monthly_coffee_sales['month'].map(month_mapping)


idx = monthly_coffee_sales.groupby(['month'])['money'].transform(max) == monthly_coffee_sales['money']
preferred_coffee_each_month = monthly_coffee_sales[idx]

st.write("### Preferred Coffee Each Month")
plt.figure(figsize=(7, 3))
sns.barplot(data=preferred_coffee_each_month, x='month_name', y='money', hue='coffee_name')
plt.title('Preferred Coffee Type Each Month')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.legend(title='Coffee Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

st.pyplot(plt)

st.markdown("""
### Overview

The bar chart titled "Preferred Coffee Type Each Month" provides a visual representation of the sales volume for each coffee type across different months. The height of each bar indicates the total sales for that particular coffee type in the corresponding month.

### Key Insights:

- **Latte Dominance**: "Latte" consistently has the highest sales volume across all months, indicating a strong preference for this coffee type.
- **Seasonal Variations**: There are noticeable seasonal variations in the sales of "Cappuccino" and "Americano with Milk." "Cappuccino" tends to have higher sales in the earlier months (March - May), while "Americano with Milk" has higher sales in the later months (July - September).
- **Consistent Sales for Americano with Milk**: "Americano with Milk" maintains relatively consistent sales throughout the year, suggesting a steady demand for this coffee type.
""")



st.divider()

# Payment Type
st.write("### Paymnet Type")
payment_type = df['cash_type'].unique()
total_sale_by_payment = df.groupby('cash_type')['money'].sum()
count_sale_by_payment = df.groupby('cash_type')['money'].count()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

ax1.pie(total_sale_by_payment, labels=total_sale_by_payment.index, autopct='%1.1f%%', startangle=140, colors=['limegreen', 'pink'])
ax1.set_title('Total Sales by Payment Type')


ax2.pie(count_sale_by_payment, labels=count_sale_by_payment.index, autopct='%1.1f%%', startangle=140, colors=['limegreen', 'pink'])
ax2.set_title('Number of Sales by Payment Type')

st.pyplot(fig)

plt.figure()
df['cash_type'].hist()
plt.title('Distribution of Cash Type')
plt.xlabel('Cash Type')
plt.ylabel('Frequency')

st.pyplot(plt)

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

st.divider()

st.write("# Conclusion")
st.write("The analysis of coffee sales reveals a significant insights on customer behavior and their preferences. “Latte” consistently emerges as the top-selling coffee, showing a strong demand for this beverage throughout the year.")
st.write("These insights imply that coffee businesses should prioritize stocking coffees like “Latte”, followed by “Americano with Milk”, and “Cappuccino”. Further analysis could investigate the impact of marketing strategies on sales and explore customer preferences of coffee types.")