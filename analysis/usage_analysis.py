import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from datetime import datetime, timedelta

"""Calculates total number of searches made at each hour over the data collection period
    and plots"""
def calculate_hourly_usage(df):
    #df = pd.read_csv(csv, parse_dates=["timestamp"])

    # Ensure the Timestamp column is in datetime format
    df["Hour"] = df["timestamp"].dt.hour  # Extract hour for hourly trends
    df["Date"] = df["timestamp"].dt.date  # Extract date for daily trends

    # Count activity per hour
    hourly_activity = df.groupby("Hour").size()

    # Plot
    plt.figure(figsize=(10, 5))
    sns.barplot(x=hourly_activity.index, y=hourly_activity.values, palette="coolwarm")
    plt.xlabel("Hour of the Day")
    plt.ylabel("Number of Searches")
    plt.title("Hourly Internet Usage")
    plt.xticks(range(0, 24))  # Ensure all 24 hours are visible
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()

def weekday_weekend_usage(df):
    df["Hour"] = df["timestamp"].dt.hour
    df["Day of Week"] = df["timestamp"].dt.dayofweek  # Monday=0, Sunday=6
    df["Category"] = df["Day of Week"].apply(lambda x: "Weekend" if x >= 5 else "Weekday")

    # Group by hour and category
    activity_by_hour = df.groupby(["Hour", "Category"]).size().unstack()

    # Plot
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=activity_by_hour, marker="o")
    plt.xlabel("Hour of the Day")
    plt.ylabel("Number of Activities")
    plt.title("Hourly Internet Usage: Weekdays vs. Weekends")
    plt.xticks(range(0, 24))
    plt.legend(title="Day Type")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()
