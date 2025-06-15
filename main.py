import asyncio
import concurrent.futures
from alpaca_trade_api.rest import REST
from strategies.MovingAverageCrossoverStrategy import MovingAverageCrossoverStrategy
from core.ExecutionEngine import ExecutionEngine
from core.RiskManager import RiskManager

API_KEY = 'PKJRJPIDCFGP6X7SNZWH'
SECRET_KEY = '0XNdOcNRtG4KOMHkDb8SZueJkfrOhTWZSGnA0Trf'
BASE_URL = 'https://paper-api.alpaca.markets'  # Make sure you're using the paper trading URL

# Initialize API client
api = REST(API_KEY, SECRET_KEY, base_url=BASE_URL)

# Define symbols to trade
symbols = ['AAPL', 'MSFT', 'GOOGL']

# Create strategy instances (multiple per symbol)
strategies = {
    symbol: [
        MovingAverageCrossoverStrategy(api, symbol, short_window=5, long_window=20)
        # Add more strategies here per symbol
    ]
    for symbol in symbols
}

# Initialize Risk Manager and Execution Engine
risk_manager = RiskManager(api)
execution_engine = ExecutionEngine(api, strategies, risk_manager)

# Start trading loop
executor = concurrent.futures.ThreadPoolExecutor()

async def execute_trade(symbol):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(executor, execution_engine.execute_symbol, symbol)

async def main():
    while True:
        tasks = [execute_trade(symbol) for symbol in symbols]
        await asyncio.gather(*tasks)
        await asyncio.sleep(60)  # Wait a minute between cycles

if __name__ == '__main__':
    print("Starting asynchronous trading loop...")
    asyncio.run(main())
