## Goal (Business requirements)

Equal weight portfolio rebalance

- We can press the Run button and our output is
  - "Stocks rebalance"
    - What does that mean?
        - We maintain a local document of our proportions. We actually buy/sell shares in our algorithm to meet this requirement.


## (Tech/Software) Components


- Algorithm
    - On start
        - Our entities: Tickers, Sectors.
            - Requirements:
                - Tickers are weighted equally by sector
                - Tickers are assigned value from spreadsheet (ticker_gics_industry.csv)
                - Sector: a group of tickers

            Data model:

                A "Balanced Portfolio" = ..

                Our Portfolio: (Proportions, portfolio.csv)
                - This is just for the "active" investments
                    - When a listing gets dropped from an exchange and we dump it, we remove from this table.
               ----------------------------------------------------------------
               | Stock ticker | Sector     | % of portfolio | % of sector | 
               ----------------------------------------------------------------
               | GOOG         | Tech       | 0.33           | 0.5         | 
               | IBM          | Tech       | 0.33           | 0.5         | 
               | XOM          | Energy     | 0.33           | 1.0         | 
               | JPM          | Financials | 0.33           | 1.0         | 
               ----------------------------------------------------------------

  - Month over month, we make a calculation ("Rebalance")

    Technical Process:

        1. We ask API "What are the tickers and prices right now?"
            - Requirement: Pull from the first trading day of the month
            - Technical challenge: Requesting too many tickers in 1 request (We can only do 20 tickers. Works for testing. Needs a solution in production)


        2. API says Google, EXOM & JPM exist. IBM does not in an error log (for that time range).

            Per our data model, this would mean we're in this state

               ----------------------------------------------------------------
               | Stock ticker | Sector     | % of portfolio | % of sector | 
               ----------------------------------------------------------------
               | IBM          | Tech       | 0.33           | 0.5         |
               | GOOG         | Tech       | 0.33           | 0.5         | 
               | XOM          | Energy     | 0.33           | 1.0         | 
               | JPM          | Financials | 0.33           | 1.0         | 
               ----------------------------------------------------------------

            Log the request result our data model

        3. We "rebalance". Now we're in a "balanced" state.

            1. Modifying the "% of sector" column in our local CSV. 
            2. Buy/Sell the difference between the two portolio percentages.
                - This needs to be togglable for testing purposes
                    - TEST mode: Do nothing
                    - PRODUCTION mode: Make an API call to buy/sell

                - Log this transaction (even though we're putting it into a CSV as well)

                e.g "I bought $50 of google, $50 of IBM. IBM dropped from exchange, so I now need to drop $50 of IBM. Buy $50 more ($100 total now) of google.

               ----------------------------------------------------------------
               | Stock ticker | Sector     | % of portfolio | % of sector | 
               ----------------------------------------------------------------
               | GOOG         | Tech       | 0.33           | 1.0         | 
               | XOM          | Energy     | 0.33           | 1.0         | 
               | JPM          | Financials | 0.33           | 1.0         | 
               ----------------------------------------------------------------

            3. Make some record of this transaction (for auditing purposes)

                transactions.csv:
            
                --------------------------------------------------------------------------
               | Stock ticker | Buy/Sell | Amount (of the stock) | Timestamp
               ---------------------------------------------------------------------------
               ...
               | IBM         | Sell       | 3                    | 1/2/2024,10pm         | 
               ---------------------------------------------------------------------------

            Some thoughts from earlier:

                - Was there a ticker added or removed in that timeframe? (That will impact our weighting of the tickers.)
                If the ticker does or does not exist, we adjust the denominator of the tickers
                (If we go from 9 stocks to 10 stocks, we now weight over 10 stocks not 9)
                - Context: Tickers can be added/removed from an exchange beyond the scope of this program
                - What is the weight on that ticker?

        4. We do some other calculations

            Goal: To have data on the outputs the algorithm over time (Net gains)

            - % Cum Ticker Return, % Cum Sector Return
                - Inputs: 
                    - "New price": Ticker value from API call (Adjusted price) (from API call in Step 2)
                    - "Old price": prices.csv
                    - % gain = ((Ticker current price - Ticker previous price)/(previous price)) 

                prices.csv: Our log of the prices as we most recently know them 

                    We use this to calculate month-to-month change.
            
                --------------------------------------------------------------------------
               | Stock ticker | Price | Timestamp (the historical ticker price)       |
               ---------------------------------------------------------------------------
               | IBM         | 123     | 1/2/2024,10pm         | 
               ---------------------------------------------------------------------------

                - Writing this into returns.csv (just for auditing-over-time purposes and checking the algo health)

                returns.csv: 
            
                TODO: Workshop this. Goal of table is to be used for testing the quality of the algo.

                --------------------------------------------------------------------------
    | Stock ticker | Stock price | Sector | Timestamp (the historical ticker price) | % Return change from last month | % Cumulative Return  | % Cumulative Sector Return  |
               ---------------------------------------------------------------------------
               ...
               | IBM         | 123     | Tech | 1/1/2024,10pm  | 0.5 | 0.2 | 0.4
               | IBM         | 125     | Tech | 2/1/2024,10pm  | (125-123)/123 | 0.2 | 0.4
               ---------------------------------------------------------------------------

    Our output: (The data tables above)

- Backtester for the algorithm (Some metric that the algorithm is measured against)
  - How did the algorithm perform?

        1. Run the algorithm on timestamp X to Y
        - Show a visual of
            - The % returns
        - To verify the balancing is done correctly, we need to use logs and they can only be verified manually.
            - The API request result (Stocks, ticker values for that timestamp)
            - The portfolio proportions
            - The adjustments made

        TODO, but we use the returns.csv file.

- Some visualization of this rebalancing?

    TODO, but did not have enought time to incorporate matplotlib and other data visualizations like scatter plots and even regressions for sector var.

#####IMPORTANT NOTE
    Additionally, I shortened the tickers_gics_industry.csv file to test a more mananable data set based on the API limit on the free version. If there is a way to cache or delay using semafore, this could be an option to pull the 14k tickers, and distill them.

If I had more time, I would think about backtesting this strategy with portfolio optimization tools and seeing how far away the skew is from certain tickers.
Adding formulas and topics of goodness of fit and mean reversion. 

Thank you for a great challenge, this was a great experience to work on and love to learn more. I would like to build off of my finance skills and python experience to grow with your team!

Best,
Sean Bajwa