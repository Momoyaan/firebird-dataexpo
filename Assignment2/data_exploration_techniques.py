import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('exercise_dataset.csv')

print("Data Types:")
print(df.dtypes)

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

    print("Mean: \n", mean)
print("Median: \n", median)
print("Mode: \n", mode)
print("Standard Deviation: \n", std_dev)
print("Variance: \n", variance)
print("Minimum: \n", min_values)
print("Maximum: \n", max_values)
print("Range: \n", range_values)
print("Percentiles: \n", percentiles)

df.hist(bins=30, figsize=(10,8))
plt.xlabel("Number of calories burned")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

plt.figure(figsize=(10,6))
sns.boxplot(data=df)
plt.title("Box plot of all calories burned")
plt.xlabel("Weight (Ibs)")
plt.ylabel("Calories burned")
plt.show()

if not numeric_df.empty:
    correlation_matrix = numeric_df.corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    plt.title("Calories Burned")
    plt.show()
else:
    print("No numeric columns avaliable for correlation analysis.")