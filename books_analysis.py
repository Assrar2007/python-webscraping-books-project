import os
import pandas as pd
import matplotlib.pyplot as plt

# 1. LOAD DATA
data_path = os.path.join("data", "books_data.csv")
df = pd.read_csv(data_path)

print("Total rows:", df.shape[0])
print("\nFirst 5 rows:")
print(df.head())

print("\nSummary of prices (price_clean):")
print(df["price_clean"].describe())

# 2. SIMPLE INSIGHTS

# a) Cheapest & costliest book
min_price = df["price_clean"].min()
max_price = df["price_clean"].max()

cheapest_book = df.loc[df["price_clean"].idxmin(), "title"]
costliest_book = df.loc[df["price_clean"].idxmax(), "title"]

print(f"\nCheapest book: {cheapest_book} -> £{min_price}")
print(f"Most expensive book: {costliest_book} -> £{max_price}")

# b) Count of books by rating
rating_counts = df["rating"].value_counts()
print("\nBooks count by rating:")
print(rating_counts)

# c) Availability counts
avail_counts = df["availability"].value_counts()
print("\nAvailability counts:")
print(avail_counts)

# 3. VISUALISATIONS
os.makedirs("charts", exist_ok=True)

# Histogram of prices
plt.figure()
df["price_clean"].hist(bins=10)
plt.title("Distribution of Book Prices")
plt.xlabel("Price (£)")
plt.ylabel("Number of Books")
plt.tight_layout()
plt.savefig(os.path.join("charts", "price_distribution.png"))

# Bar chart for rating counts
plt.figure()
rating_counts.plot(kind="bar")
plt.title("Number of Books by Rating")
plt.xlabel("Rating")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(os.path.join("charts", "rating_counts.png"))

# Bar chart for availability
plt.figure()
avail_counts.plot(kind="bar")
plt.title("Availability of Books")
plt.xlabel("Availability Status")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(os.path.join("charts", "availability_counts.png"))

print("\nCharts saved in 'charts' folder:")
print(" - price_distribution.png")
print(" - rating_counts.png")
print(" - availability_counts.png")
