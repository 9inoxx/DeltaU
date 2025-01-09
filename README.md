# DeltaU

DeltaU is a backtesting and performance analysis package for quantitative trading strategies.

## Installation

You can install DeltaU using `pip install DeltaU':


## Usage

Example usage:

```python
import pandas as pd
from deltau.core.backtester import Backtester, Executor
from deltau.visualization.tear_sheet import TearSheet

# Create a DataFrame 
data = pd.read_csv('stock_data.csv')

# Create a strategey and generate signals
class ExampleStrategy:
    def generate_signals(self, data):
        # Calculate short and long moving averages
        data['Short_MA'] = data['Close'].rolling(window=5).mean()
        data['Long_MA'] = data['Close'].rolling(window=20).mean()
        
        # Generate signals: 1 for Buy, -1 for Sell, 0 for Hold
        signals = (data['Short_MA'] > data['Long_MA']).astype(int).diff()
        return signals

# Instantiate the strategy, executor, and backtester
strategy = ExampleStrategy(window=self.window)
executor = Executor(initial_capital=600, share_size=10)
backtester = Backtester(strategy=strategy, executor=executor, data=data)

# Run the backtest
portfolio_values, final_metrics = backtester.run()

# Create a TearSheet object with the results and metrics
tear_sheet = TearSheet(backtest_results=portfolio_values, metrics=final_metrics)

# Generate the report and show plots
tear_sheet.display_report()

## In case you get an error when calling tear_sheet function while using jupyter

Copy and paste: pip install nbformat>=4.2.0 into your envrionment, restart the environment and than re-run the code.

**Note**: Ensure your CSV data includes the following columns: 
- `Date`: The trading date (ensure it’s in a recognizable datetime format).
- `Open`, `High`, `Low`, `Close`: Standard OHLC prices for each trading day.
- `Adj Close`: Adjusted close price accounting for corporate actions like splits/dividends.
- `Volume`: Trading volume for the day.

# I've tried my best to make things as simple as calling strategy = ExampleStrategy(window=self.window) executor = Executor(initial_capital=600, share_size=10) backtester = Backtester(strategy=strategy, executor=executor, data=data)>

# In order for the simulation to run successfully each strategy needs to generate a 1 (buy), -1 (sell), or 0 (hold) signal.
