import pandas as pd
import os
from collections import defaultdict

def compile_monthly_csvs(data_directory):
    # Dictionary to hold DataFrames for each month
    monthly_data = defaultdict(list)

    # List all files in the data directory
    for file_name in os.listdir(data_directory):
        if file_name.endswith('.csv'):
            # Read the CSV file
            file_path = os.path.join(data_directory, file_name)
            df = pd.read_csv(file_path)

            # Extract date information from the file name if needed
            # _, ticker, date_str = file_name.split('_')
            # year_month = date_str[:7]  # Assumes format is YYYYMMDD

            # Append the DataFrame to the list for its month
            # Assumes the file name includes the year and month as the first 7 characters
            year_month = file_name[:7] 
            monthly_data[year_month].append(df)

    # For each month, concatenate all DataFrames and save to a new CSV
    for year_month, dataframes in monthly_data.items():
        if dataframes:
            combined_df = pd.concat(dataframes, ignore_index=True)

            # Group by 'ticker' and 'Sector', then sum the 'Cumulative Return'
            final_df = combined_df.groupby(['ticker', 'Sector'], as_index=False)['Cumulative Return'].transform('sum')

            # Define output file name
            output_file_name = f"compiled_data_{year_month}.csv"
            output_file_path = os.path.join(data_directory, output_file_name)

            # Save the final DataFrame
            final_df.to_csv(output_file_path, index=False)
            print(f"Saved compiled data for {year_month} to {output_file_path}")

# Example usage
data_directory = "data/rebalanced_return"  # Update this path to your data directory
compile_monthly_csvs(data_directory)


