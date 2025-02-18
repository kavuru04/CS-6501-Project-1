import pandas as pd
from analysis.usage_analysis import calculate_hourly_usage, weekday_weekend_usage
from analysis.sleep_analysis import analyze_sleep_patterns, print_sleep_analysis, sleep_disruptions

def main():
    # Load data
    df = pd.read_csv("parsed_timestamps.csv", parse_dates=["timestamp"])

    # Perform basic usage analysis
    calculate_hourly_usage(df)
    weekday_weekend_usage(df)

    # Sleep analysis
    stats, sleep_periods = analyze_sleep_patterns("parsed_timestamps.csv")
    print_sleep_analysis(stats, sleep_periods)

    # Given results of Sleep analysis calculate number of sleep disruptions
    sleep_disruptions(df)

if __name__ == "__main__":
    main()
