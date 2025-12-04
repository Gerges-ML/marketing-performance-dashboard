import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Marketing Dashboard", layout="wide")

st.title("📊 Marketing Performance Dashboard")
st.write("قم برفع ملف الحملات التسويقية (Excel) لتحليل الأداء وعرض النتائج")

# ====================== FILE UPLOAD ======================
uploaded_file = st.file_uploader("📂 Upload Excel File", type=["xlsx"])

if uploaded_file is not None:

    df = pd.read_excel(uploaded_file)

    df.columns = [c.strip() for c in df.columns]
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    for col in ["Ad Spend", "Conversions", "Revenue"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["Date"]).reset_index(drop=True)
    df["Month"] = df["Date"].dt.to_period("M").astype(str)

    df["CAC"] = df.apply(lambda r: r["Ad Spend"] / r["Conversions"] if r["Conversions"] > 0 else np.nan, axis=1)
    df["ROI"] = df.apply(lambda r: r["Revenue"] / r["Ad Spend"] if r["Ad Spend"] > 0 else np.nan, axis=1)

    # ====================== GROUP BY ======================
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

    # ====================== SHOW DATA ======================
    st.subheader("📄 Raw Data Preview")
    st.dataframe(df.head())

    # ====================== VISUALIZATIONS ======================

    # Bar chart – Total Conversions per Channel
    st.subheader("📈 Total Conversions per Channel")
    fig1, ax1 = plt.subplots(figsize=(8,5))
    ax1.bar(by_channel["Channel"], by_channel["Total_Conversions"])
    ax1.set_title("Total Conversions per Channel")
    ax1.tick_params(axis='x', rotation=30)
    st.pyplot(fig1)

    # Bar chart – Revenue per Channel
    st.subheader("💰 Total Revenue per Channel")
    fig2, ax2 = plt.subplots(figsize=(8,5))
    ax2.bar(by_channel["Channel"], by_channel["Total_Revenue"])
    ax2.set_title("Total Revenue per Channel")
    ax2.tick_params(axis='x', rotation=30)
    st.pyplot(fig2)

    # Line chart – Monthly Revenue Trend
    st.subheader("📉 Monthly Revenue Trend")
    fig3, ax3 = plt.subplots(figsize=(8,5))
    ax3.plot(by_month["Month"], by_month["Total_Revenue"], marker="o")
    ax3.set_title("Monthly Revenue Trend")
    ax3.tick_params(axis='x', rotation=45)
    st.pyplot(fig3)

    # Bar chart – Average CAC
    st.subheader("📌 Average CAC per Channel")
    fig4, ax4 = plt.subplots(figsize=(8,5))
    ax4.bar(by_channel["Channel"], by_channel["Avg_CAC"])
    ax4.set_title("Average CAC by Channel")
    ax4.tick_params(axis='x', rotation=30)
    st.pyplot(fig4)

    # Bar chart – ROI
    st.subheader("📌 Average ROI per Channel")
    fig5, ax5 = plt.subplots(figsize=(8,5))
    ax5.bar(by_channel["Channel"], by_channel["Avg_ROI"])
    ax5.set_title("Average ROI by Channel")
    ax5.tick_params(axis='x', rotation=30)
    st.pyplot(fig5)

    # Pie chart – Customer Revenue Share
    st.subheader("🧮 Revenue Share by Customer Type")
    fig6, ax6 = plt.subplots(figsize=(6,6))
    ax6.pie(by_customer["Total_Revenue"], labels=by_customer["Customer Type"], autopct="%1.1f%%", startangle=90)
    ax6.set_title("Revenue Share by Customer Type")
    st.pyplot(fig6)

    # Scatter – Ad Spend vs Revenue
    st.subheader("📊 Ad Spend vs Revenue (by Channel)")
    fig7, ax7 = plt.subplots(figsize=(8,5))
    ax7.scatter(by_channel["Total_Ad_Spend"], by_channel["Total_Revenue"], s=200)
    for i, row in by_channel.iterrows():
        ax7.annotate(row["Channel"], (row["Total_Ad_Spend"], row["Total_Revenue"]))
    ax7.set_xlabel("Total Ad Spend")
    ax7.set_ylabel("Total Revenue")
    ax7.set_title("Ad Spend vs Revenue")
    st.pyplot(fig7)

    # ====================== SUMMARY ======================
    st.subheader("📌 Summary Insights")

    st.write("### ⭐ Top Channels by Conversions")
    st.dataframe(by_channel.sort_values("Total_Conversions", ascending=False).head(3))

    st.write("### 💰 Top Channels by Revenue")
    st.dataframe(by_channel.sort_values("Total_Revenue", ascending=False).head(3))

    st.write("### 📈 Best ROI Channels")
    st.dataframe(by_channel.sort_values("Avg_ROI", ascending=False).head(3))

    st.write("### ⚠️ Worst Channels (Highest CAC)")
    st.dataframe(by_channel.sort_values("Avg_CAC", ascending=False).head(3))

else:
    st.info("⬆️ رجاءً قم برفع ملف Excel لبدء التحليل.")
