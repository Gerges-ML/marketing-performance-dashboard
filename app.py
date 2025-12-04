import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_path = "01KA425CSA9DEYNBC769P5BNH3.xlsx"
df = pd.read_excel(file_path)

df.columns = [c.strip() for c in df.columns]
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

for col in ["Ad Spend", "Conversions", "Revenue"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=["Date"]).reset_index(drop=True)

df["Month"] = df["Date"].dt.to_period("M").astype(str)

df["CAC"] = df.apply(lambda r: r["Ad Spend"] / r["Conversions"] if r["Conversions"] > 0 else np.nan, axis=1)
df["ROI"] = df.apply(lambda r: r["Revenue"] / r["Ad Spend"] if r["Ad Spend"] > 0 else np.nan, axis=1)

by_channel = df.groupby("Channel").agg(
    Total_Ad_Spend=("Ad Spend", "sum"),
    Total_Conversions=("Conversions", "sum"),
    Total_Revenue=("Revenue", "sum"),
    Avg_CAC=("CAC", "mean"),
    Avg_ROI=("ROI", "mean"),
).reset_index()

by_month = df.groupby("Month").agg(
    Total_Ad_Spend=("Ad Spend", "sum"),
    Total_Conversions=("Conversions", "sum"),
    Total_Revenue=("Revenue", "sum"),
    Avg_CAC=("CAC", "mean"),
    Avg_ROI=("ROI", "mean"),
).reset_index()

by_customer = df.groupby("Customer Type").agg(
    Total_Revenue=("Revenue", "sum")
).reset_index()


# ===================== SAVE VISUALIZATIONS =====================

plt.figure(figsize=(10,6))
plt.bar(by_channel["Channel"], by_channel["Total_Conversions"])
plt.title("Total Conversions per Channel")
plt.xlabel("Channel")
plt.ylabel("Conversions")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("total_conversions_per_channel.png", dpi=300, bbox_inches="tight")
plt.show()

plt.figure(figsize=(10,6))
plt.bar(by_channel["Channel"], by_channel["Total_Revenue"])
plt.title("Total Revenue per Channel")
plt.xlabel("Channel")
plt.ylabel("Revenue (USD)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("total_revenue_per_channel.png", dpi=300, bbox_inches="tight")
plt.show()

plt.figure(figsize=(10,6))
plt.plot(by_month["Month"], by_month["Total_Revenue"], marker="o")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (USD)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("monthly_revenue_trend.png", dpi=300, bbox_inches="tight")
plt.show()

plt.figure(figsize=(10,6))
plt.bar(by_channel["Channel"], by_channel["Avg_CAC"])
plt.title("Average CAC by Channel")
plt.xlabel("Channel")
plt.ylabel("CAC (USD)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("avg_cac_by_channel.png", dpi=300, bbox_inches="tight")
plt.show()

plt.figure(figsize=(10,6))
plt.bar(by_channel["Channel"], by_channel["Avg_ROI"])
plt.title("Average ROI by Channel")
plt.xlabel("Channel")
plt.ylabel("ROI")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("avg_roi_by_channel.png", dpi=300, bbox_inches="tight")
plt.show()

plt.figure(figsize=(8,6))
plt.pie(by_customer["Total_Revenue"], labels=by_customer["Customer Type"], autopct="%1.1f%%", startangle=90)
plt.title("Revenue Share by Customer Type")
plt.tight_layout()
plt.savefig("revenue_share_by_customer_type.png", dpi=300, bbox_inches="tight")
plt.show()

plt.figure(figsize=(10,6))
plt.scatter(by_channel["Total_Ad_Spend"], by_channel["Total_Revenue"], s=200)
for i, row in by_channel.iterrows():
    plt.annotate(row["Channel"], (row["Total_Ad_Spend"], row["Total_Revenue"]))
plt.title("Ad Spend vs Revenue (by Channel)")
plt.xlabel("Total Ad Spend (USD)")
plt.ylabel("Total Revenue (USD)")
plt.tight_layout()
plt.savefig("ad_spend_vs_revenue.png", dpi=300, bbox_inches="tight")
plt.show()


# ===================== SUMMARY PRINT =====================

print("\n================ SUMMARY ================\n")
print("Top Channels by Conversions:")
print(by_channel.sort_values("Total_Conversions", ascending=False).head(3), "\n")

print("Top Channels by Revenue:")
print(by_channel.sort_values("Total_Revenue", ascending=False).head(3), "\n")

print("Best ROI Channels:")
print(by_channel.sort_values("Avg_ROI", ascending=False).head(3), "\n")

print("Highest CAC Channels (Worst):")
print(by_channel.sort_values("Avg_CAC", ascending=False).head(3), "\n")
