#Final Output
import os
import pandas as pd
import glob

# Function to load and preprocess CSV files
def load_and_preprocess(file_path):
    df = pd.read_csv(file_path)
    # Add preprocessing steps here if needed
    return df

# Function to compile cumulative returns
def compile_cumulative_returns(folder_path):
    # Find all CSV files in the folder
    csv_files = glob.glob(folder_path + '/*.csv')

    if not csv_files:
        print("No CSV files found in the configured directory.")
        return

    # Load and preprocess each CSV file
    list_of_df = [load_and_preprocess(file) for file in csv_files]

    # Combine all DataFrames into one
    combined_df = pd.concat(list_of_df, ignore_index=True)

    # Aggregate cumulative returns by ticker
    final_df = combined_df.groupby(['ticker'])['Cumulative Return'].sum().reset_index()

    # Define the new output directory
    output_directory = os.path.join(folder_path, '../rebalanced_return')

    # Ensure the new output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Define the output file path in the new directory
    output_file = os.path.join(output_directory, 'compiled_cumulative_returns.csv')

    # Save the final DataFrame
    final_df.to_csv(output_file, index=False)
    print(f"Compiled data saved to: {output_file}")

# Example usage
if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.abspath(__file__))
    data_folder_relative_path = 'data'
    data_folder_path = os.path.join(script_directory, data_folder_relative_path)
    compile_cumulative_returns(data_folder_path)
