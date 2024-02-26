import os
import pandas as pd
from csv_util import load_csv, save_csv
from balancing_logic import initialize_weights, calculate_rebalance_actions
from data_fetching import fetch_prices
from Final_Output import compile_cumulative_returns

def run_initialization():
    print("Running portfolio initialization...")
    
    # Initialize the portfolio with weights
    portfolio_data = initialize_weights()
    
    # Define the path for saving the portfolio CSV file
    current_directory = os.path.dirname(os.path.abspath(__file__))
    portfolio_file_path = os.path.join(current_directory, 'finance_logic', 'portfolio.csv')
    
    # Define the CSV header field names
    fieldnames = ['ticker', 'Sector', 'Percentage of portfolio', 'Percentage of sector']
    
    # Save the initialized portfolio to a CSV file
    save_csv(portfolio_file_path, portfolio_data, fieldnames)
    print("Portfolio initialized and saved to", portfolio_file_path)

def monthly_rebalance():
    print("Running monthly rebalance...")

    #Open up init CSV w/ Portfolio info
    current_portfolio = pd.read_csv("finance_logic/portfolio.csv")
    
    #.. for each ticker in portfolio we need to check if it exists, and its price if it exists 

    # Create a loop that gets all of the tickers from one perdiod of time to another:
    
    # Time Period for historical data
    start_date = '2016-01-02'
    end_date = '2017-01-02'

    tickers = current_portfolio['ticker'].tolist()
    market_data_frames = fetch_prices(tickers, start_date, end_date)
    
    # Now you have an array of pandas DataFrames containing data for each ticker symbol
    # You can further process or analyze these DataFrames as needed
    #for i, df in enumerate(market_data_frames):
    #    print(f"DataFrame for {tickers[i]}:")
    #    print(df.head())  # Print the first few rows of each DataFrame  

    #print(market_data_frames)
    
    updated_portfolio_data = calculate_rebalance_actions(current_portfolio, market_data_frames)
    
    output_path = 'data/'  # Assuming the data folder is in the following structure

    compile_cumulative_returns(output_path)


    #Adjust fieldnames to include all keys used in updated_portfolio_data
    #fieldnames = ['TICKER', 'Date', 'Sector', 'Percentage of portfolio', 'Percentage of sector', 'Action', 'Price']
    
    #new_portfolio_file_path = os.path.join(current_directory, 'finance_logic', 'rebal portfolio.csv')
    #save_csv(new_portfolio_file_path, updated_portfolio_data, fieldnames)
    #print("Rebalanced portfolio saved to", new_portfolio_file_path)