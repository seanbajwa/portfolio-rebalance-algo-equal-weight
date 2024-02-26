####This module will calculate the initial weights for each sector and prepare the initial portfolio data structure.
# balancing_logic.py
from datetime import date, datetime
import pandas as pd
import os

# Assuming csv_util.load_csv is a function you've defined to load CSV files
from csv_util import load_csv

# Inside finance_logic/balancing_logic.py
def initialize_weights():
    # Define the path to the ticker data
    current_directory = os.path.dirname(os.path.abspath(__file__))
    ticker_file_path = os.path.join(current_directory, 'ticker_gics_industry.csv')

    # Load the ticker data
    ticker_data = load_csv(ticker_file_path)

    sectors = {row['Sector'] for row in ticker_data if row['Sector']}
    sector_weight = 1 / len(sectors) if sectors else 0

    # Count tickers per sector and assign weight per ticker
    portfolio_data = []
    for sector in sectors:
        sector_tickers = [row for row in ticker_data if row['Sector'] == sector]
        ticker_weight_in_sector = sector_weight / len(sector_tickers) if sector_tickers else 0

        for row in sector_tickers:
            portfolio_data.append({
                'ticker': row['TICKER'],
                'Sector': sector,
                'Percentage of portfolio': ticker_weight_in_sector,
                'Percentage of sector': 1 / len(sector_tickers) if sector_tickers else 0
            })

    return portfolio_data

# Add functionality to calculate rebalancing actions based on the fetched market data and current portfolio state
def calculate_rebalance_actions(current_portfolio, market_data_frames):
    current_portfolio = current_portfolio.drop_duplicates(subset=['ticker'])
    rebalance_actions = []

    # Rebalance variables
    new_port_perc = 0
    new_sect_perc = 0

    # Iterate over each ticker dataframe in the list
    for df in market_data_frames:
        # Convert 'index' column to datetime format for each dataframe
        df['index'] = pd.to_datetime(df['index'])

        ticker_price_history = []

        # Group ticker data by date and iterate through each date
        for index, group in df.groupby(df['index']):
            current_ticker = group['ticker'].iloc[0]
            current_ticker_price = group[current_ticker].iloc[0]  # Assuming 'close' is the closing price
            ticker_price_history.append(current_ticker_price)

            ticker_info = current_portfolio[current_portfolio['ticker'] == current_ticker]
            sector = current_portfolio.loc[current_portfolio['ticker'] == current_ticker, 'Sector'].values[0]
            combined_df = pd.merge(ticker_info, group, on='ticker', how='left')

            if len(ticker_price_history) == 1:
                new_port_perc = 1.2  # Placeholder for new portfolio percentage logic
                new_sect_perc = 1.2  # Placeholder for new sector percentage logic
                difference_Data = {
                    'ticker': [current_ticker],
                    'Previous Price': [0.00],  # Placeholder for previous price
                    'Monthly Percentage': [0.00],  # Placeholder for monthly percentage change
                    'Cumulative Return': [0.00]  # Placeholder for cumulative return
                }
            else:
                prev_price = ticker_price_history[-2]
                pnl = (current_ticker_price - prev_price) / prev_price
                cum_return = pnl * new_port_perc

                difference_Data = {
                    'ticker': [current_ticker],
                    'Previous Price': [prev_price],
                    'Monthly Percentage': [pnl],
                    'Cumulative Return': [cum_return]
                }

            df_difference = pd.DataFrame(difference_Data)
            df_difference['Sector'] = sector  # Here we assign the sector
            combined_df = pd.merge(combined_df, df_difference, on=['ticker', 'Sector'],how='left')

            # Define the base directory where you want to save the CSV files
            base_directory = "data"
            if not os.path.exists(base_directory):
                os.makedirs(base_directory)

            # Define the file path for the CSV file with the current date
            file_path = os.path.join(base_directory, f"data_{current_ticker}_{index.strftime('%Y%m%d')}.csv")

            # Save the combined DataFrame to the CSV file
            combined_df.to_csv(file_path, index=False)

#SAVEE
# Example usage
# Assuming `current_portfolio` and `market_data_frames` are defined elsewhere
# current_portfolio = pd.DataFrame(...)  # Your current portfolio DataFrame
# market_data_frames = [pd.DataFrame(...), ...]  # List of market data DataFrames
# calculate_rebalance_actions(current_portfolio, market_data_frames)


   # for stock in current_portfolio:
    #    ticker = stock['TICKER']
     #   if ticker in market_data_dict:
      #      df = market_data_dict[ticker]
       #     # Assuming the DataFrame has 'date' as a column after resetting index in `fetch_prices`
        #    for index, row in df.iterrows():
            # Ensure 'date' is in datetime format and then format it as a string
         #       date_of_price = row['date'].strftime('%Y-%m-%d') if pd.notnull(row['date']) else 'N/A'
          #      current_price = row['adjClose']
          #      action = 'BUY' if current_price < 100000000 else 'SELL'
          #      rebalance_actions.append({
          #      'TICKER': ticker,
          #      'Date': date_of_price,
          #      'Sector': stock['Sector'],
          #      'Percentage of portfolio': stock['Percentage of portfolio'],
          #      'Percentage of sector': stock['Percentage of sector'],
          #      'Action': action,
          #      'Price': current_price,})
       # else:
    #        print(f"No market data found for {ticker}. Defaulting to SELL.")
    #        rebalance_actions.append({
    #            'TICKER': ticker,
              #  'Date': 'N/A',
    #            'Action': 'SELL',
             #   'Price': 'N/A',
    #        })
    return rebalance_actions


















































    # Convert list of DataFrames into a dictionary for easier access
    #market_data_dict = {df['ticker'].iloc[0]: df for df in market_data_frames}

    # Example logic to calculate rebalance actions
    ##for stock in current_portfolio:
      ##  ticker = stock['TICKER']
        ##sector = stock['Sector']
        ##perc_Port = stock['Percentage of portfolio']
        ##perc_sector = stock['Percentage of sector']
        # Placeholder logic - in reality, this would involve more complex calculations
        # based on the difference between the current and desired weighting

        ##df = market_data_dict.get(ticker)

        ##current_price = market_data.get(ticker, 100)
        ##if current_price < 200:  # Assuming buying opportunity if below a threshold
          #  action = 'BUY'
        #else:
         #   action = 'SELL'

        #rebalance_actions.append({'TICKER': ticker,'Sector': sector,'Percentage of portfolio': perc_Port,'Percentage of sector': perc_sector, 'Action': action, 'Price': current_price})

    #return rebalance_actions


