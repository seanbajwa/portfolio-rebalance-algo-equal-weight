import pandas as pd
from tiingo import TiingoClient
from datetime import datetime


def fetch_prices(tickers, start_date, end_date):
    """
    Fetches data for multiple ticker symbols using the Tiingo API and returns an array of pandas DataFrames.

    Args:
    - ticker_symbols (list): List of ticker symbols to fetch data for.
    - start_date (str): Start date in the format 'YYYY-MM-DD'.
    - end_date (str): End date in the format 'YYYY-MM-DD'.
    - api_key (str): Tiingo API key.

    Returns:
    - list: Array of pandas DataFrames containing fetched data for each ticker symbol.
    """

    # Initialize Tiingo client with API key
    config = {
        'session': True,
        'api_key': '4275ac9f1e202f2125d55a7b486d5c13d32ad2e5'  
    }
    client = TiingoClient(config)

    # Initialize an empty list to store DataFrames
    dfs = []


    for ticker in tickers:
        try:
            # Even though we're querying one ticker at a time, we specify metric_name due to API requirements
            df = client.get_dataframe(tickers=[ticker],
                                        startDate=start_date,
                                        endDate=end_date,
                                        frequency='monthly',
                                        metric_name='adjClose')  # Include metric_name here
            
            # Resetting the index to make 'date' a column, assuming data is returned with 'date' as the index
            df.reset_index(inplace=True)
            df['ticker'] = ticker  # Add ticker column
            dfs.append(df)
        except Exception as e:
            pass

    return dfs    

def filter_for_first_trading_day(dfs):
    first_trading_days = []
    for df in dfs:
        # Convert 'date' column to datetime format
        df['date'] = pd.to_datetime(df['date'])
        # Set 'date' column as the DataFrame's index
        df.set_index('date', inplace=True)
        # Ensure DataFrame is sorted by date
        df.sort_index(inplace=True)
        # Resample to monthly frequency, selecting the first day in each group
        monthly_first_days = df.resample('MS').first()
        # Reset index to make 'date' a column again, if needed
        monthly_first_days.reset_index(inplace=True)
        first_trading_days.append(monthly_first_days)
    return first_trading_days    
       
   
        #if not 'date' in ticker_history.columns:
         #   ticker_history.reset_index(level=0, inplace=True)
            
            # Ensure 'date' is present as a column now
          #  if 'date' in ticker_history.columns:
                # Add a 'ticker' column to the DataFrame
           #     ticker_history['ticker'] = ticker
      #          dfs.append(ticker_history[['date', 'adjClose', 'ticker']])
           # else:
            #    print(f"Missing 'date' column in data for {ticker}")

    #except Exception as e:
     #   print(f"Error fetching data for {ticker}: {e}")
        
    
    # return dfs 


