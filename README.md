# DeltaU

DeltaU is a backtesting and performance analysis package for quantitative trading strategies.

## Installation

You can install DeltaU using `pip install DeltaU':


## Usage

Example usage:

```python
from deltau.core.backtester import Backtester, Executor
from deltau.visualization.tear_sheet import TearSheet

# Create a strategey and generate signals
def class MyStrategy:
     def __init__(self, window=1):
        self.window = window
        
        def generate_signals(self, data):
            #generate signals

             return signals

# Instantiate the strategy, executor, and backtester
strategy = MyStrategy(window=self.window)
executor = Executor(initial_capital=initial_capital)
backtester = Backtester(strategy=strategy, executor=executor, data=data)

# Run the backtest
portfolio_values, final_metrics = backtester.run()

# Create a TearSheet object with the results and metrics
tear_sheet = TearSheet(backtest_results=portfolio_values, metrics=final_metrics)

# Generate the report and show plots
tear_sheet.display_report()

## In case you get an error when calling tear_sheet function while using jupyter 
## Copy and paste: pip install nbformat>=4.2.0 into your envrionment, restart the environment and than re-run the code.

