import random
ENV = 'test'

async def fetch_data(session, ticker, api_key, dates, sem):
    url = f"https://api.tiingo.com/tiingo/daily/{ticker}/prices?startDate={start_date}&endDate={end_date}&token={api_key}"
    async with sem, session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            return {ticker: data}
        else:
            logging.warning(f"Failed to fetch data for {ticker}: HTTP {response.status}")
            return {ticker: None}

async def fetch_all_data(tickers, api_key, dates):
    sem = Semaphore(10)  # Adjust based on your API's rate limit
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, ticker, api_key, dates, sem) for ticker in tickers]
        results = await asyncio.gather(*tasks)
        return dict(zip(tickers, results))

async def fetch_data(session, ticker, api_key, dates, sem):
    if ENV == 'test':
        return [{
		"adjClose": random.randint(100, 200),
		"adjHigh": random.randint(100, 200),
		"adjLow": random.randint(100, 200),
		"adjOpen": random.randint(100, 200),
		"adjVolume": 21865118,
		"close": random.randint(100, 200),
		"date": "2024-02-16T00:00:00+00:00",
		"divCash": 0.0,
		"high": random.randint(100, 200),
		"low": random.randint(100, 200),
		"open": random.randint(100, 200),
		"splitFactor": 1.0,
		"volume": 21865118
	}]
    url = f"https://api.tiingo.com/tiingo/daily/{ticker}/prices?startDate={start_date}&endDate={end_date}&token={api_key}"
    async with sem, session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            return {ticker: data}
        else:
            logging.warning(f"Failed to fetch data for {ticker}: HTTP {response.status}")
            return {ticker: None}