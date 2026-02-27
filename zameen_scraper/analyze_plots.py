import pandas as pd

# 1. LOAD the data you just scraped
df = pd.read_csv("johar_town_plots.csv")

# 2. CALCULATE Key Metrics
# We remove rows where Marla might be missing to get an accurate average
df_clean = df.dropna(subset=['Marla', 'Price_Per_Marla'])

avg_price = df_clean['Price_PKR'].mean()
avg_rate_per_marla = df_clean['Price_Per_Marla'].mean()
cheapest_plot = df_clean.loc[df_clean['Price_PKR'].idxmin()]
most_expensive_plot = df_clean.loc[df_clean['Price_PKR'].idxmax()]

# 3. REPORT the findings
print("--- Johar Town Market Report ---")
print(f"Total Plots Scraped: {len(df)}")
print(f"Average Plot Price:  PKR {avg_price:,.0f}")
print(f"Average Rate/Marla:  PKR {avg_rate_per_marla:,.0f}")
print("-" * 30)
print(f"Cheapest Plot: {cheapest_plot['Price_Raw']} in {cheapest_plot['Location']}")
print(f"Priciest Plot: {most_expensive_plot['Price_Raw']} - {most_expensive_plot['Title']}")

# 4. GROUPING (The Power Move)
# Let's see the average price for 5 Marla vs 10 Marla plots specifically
summary = df_clean.groupby('Marla')['Price_PKR'].mean().astype(int)
print("\nAverage Price by Size:")
print(summary)