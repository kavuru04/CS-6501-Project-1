import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from datetime import datetime, timedelta

def analyze_sleep_patterns(csv_file):
    """
    Analyze internet browsing data to infer sleep patterns based on periods of inactivity.

    Parameters:
    csv_file (str): Path to CSV file containing browsing data with timestamp column

    Returns:
    dict: Statistics about inferred sleep patterns
    """
    df = pd.read_csv(csv_file)

    # Convert timestamp string to datetime object
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Sort by timestamp
    df = df.sort_values('timestamp')

    # Calculate time differences between consecutive events
    df['time_diff'] = df['timestamp'].diff()

    # Find gaps of 5+ hours (300 minutes)
    sleep_periods = df[df['time_diff'] > timedelta(hours=5)].copy()

    # Calculate when each sleep period started and ended
    sleep_periods['sleep_start'] = df['timestamp'].shift(1)[sleep_periods.index]
    sleep_periods['sleep_end'] = df['timestamp'][sleep_periods.index]
    sleep_periods['duration'] = sleep_periods['time_diff']

    # Extract hour of day for sleep start and end
    sleep_periods['start_hour'] = sleep_periods['sleep_start'].dt.hour
    sleep_periods['end_hour'] = sleep_periods['sleep_end'].dt.hour

    # Calculate statistics
    stats = {
        'average_sleep_duration': sleep_periods['duration'].mean(),
        'median_sleep_duration': sleep_periods['duration'].median(),
        'average_sleep_start': sleep_periods['start_hour'].mean(),
        'average_sleep_end': sleep_periods['end_hour'].mean(),
        'most_common_sleep_start': sleep_periods['start_hour'].mode().iloc[0],
        'most_common_sleep_end': sleep_periods['end_hour'].mode().iloc[0],
        'total_sleep_periods': len(sleep_periods),
        'sleep_duration_std': sleep_periods['duration'].std()
    }

    return stats, sleep_periods


def format_timedelta(td):
    """Convert timedelta to hours and minutes string"""
    total_minutes = td.total_seconds() / 60
    hours = int(total_minutes // 60)
    minutes = int(total_minutes % 60)
    return f"{hours}h {minutes}m"


def print_sleep_analysis(stats, sleep_periods):
    """Print formatted analysis results"""
    print("\nSleep Pattern Analysis Results:")
    print("-" * 40)
    print(f"Total number of detected sleep periods: {stats['total_sleep_periods']}")
    print(f"\nAverage sleep duration: {format_timedelta(stats['average_sleep_duration'])}")
    print(f"Median sleep duration: {format_timedelta(stats['median_sleep_duration'])}")
    print(f"Standard deviation: {format_timedelta(stats['sleep_duration_std'])}")
    print(f"\nTypical sleep time: {int(stats['average_sleep_start'])}:00")
    print(f"Typical wake time: {int(stats['average_sleep_end'])}:00")
    print(f"\nMost common sleep time: {int(stats['most_common_sleep_start'])}:00")
    print(f"Most common wake time: {int(stats['most_common_sleep_end'])}:00")

    # Print example sleep periods
    print("\nRecent sleep periods:")
    recent_periods = sleep_periods.tail(5)
    for _, period in recent_periods.iterrows():
        print(f"\nFrom: {period['sleep_start'].strftime('%Y-%m-%d %H:%M')}")
        print(f"To: {period['sleep_end'].strftime('%Y-%m-%d %H:%M')}")
        print(f"Duration: {format_timedelta(period['duration'])}")


def sleep_disruptions(df):
    df["Hour"] = df["timestamp"].dt.hour
    df["Day of Week"] = df["timestamp"].dt.dayofweek  # Monday=0, Sunday=6
    df["Category"] = df["Day of Week"].apply(lambda x: "Weekend" if x >= 5 else "Weekday")

    SLEEP_START = 0  # 12 AM
    SLEEP_END = 10  # 10 AM

    # Flag sleep disruptions: Any activity within the defined sleep range
    df["Sleep Disruption"] = df["Hour"].apply(lambda x: 1 if (SLEEP_START <= x <= 23) or (0 <= x < SLEEP_END) else 0)

    # Count disruptions per night
    sleep_disruptions = df[df["Sleep Disruption"] == 1].groupby("Date").size()

    # Plot sleep disruptions over time
    plt.figure(figsize=(12, 5))
    sns.barplot(x=sleep_disruptions.index, y=sleep_disruptions.values, palette="coolwarm")
    plt.xticks(ticks=range(0, len(sleep_disruptions), 50), labels=sleep_disruptions.index[::50], rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Number of Sleep Disruptions")
    plt.title("Sleep Disruptions from Late-Night Internet Activity")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()
