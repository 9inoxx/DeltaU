import pandas as pd
import numpy as np
from abc import ABC, abstractmethod

class BaseModel(ABC):
    """Abstract base class for trading models."""

    @abstractmethod
    def fit(self, X, y):
        pass

    @abstractmethod
    def predict(self, X):
        pass

class Executor:
    """Handles portfolio management and trade execution with fixed share size."""

    def __init__(self, initial_capital: float = 10000, share_size: int = 1):
        """
        Initializes the Executor with an initial capital value and defines share size for trades.

        :param initial_capital: The starting capital for the portfolio (default is 10,000).
        :param share_size: The number of shares to buy or sell per trade (default is 1).
        """
        self.initial_capital = initial_capital
        self.available_capital = initial_capital  # Track the capital available for trading
        self.shares_held = 0  # Track the number of shares owned
        self.share_size = share_size  # The number of shares to buy/sell per trade

    def execute_trade(self, action: str, price: float) -> None:
        """
        Executes a trade (buy or sell) with a fixed share size and adjusts available capital and shares held.

        :param action: The action to perform ('buy' or 'sell').
        :param price: The price at which the trade is executed.
        """
        if action == "buy":
            # Calculate capital required for the trade based on share size
            capital_required = self.share_size * price

            # Check if there's enough capital to execute the buy
            if capital_required <= self.available_capital:
                self.shares_held += self.share_size  # Increase shares held
                self.available_capital -= capital_required  # Deduct the capital used for buying
                print(f"Buying {self.share_size} shares at {price} each for {capital_required} total.")
            else:
                print(f"Not enough capital to execute buy order. Capital required: {capital_required}, Available capital: {self.available_capital}")

        elif action == "sell":
            if self.shares_held >= self.share_size:
                self.shares_held -= self.share_size  # Decrease shares held
                total_sale_value = self.share_size * price  # Capital received from selling shares
                self.available_capital += total_sale_value  # Add the capital from the sale
                print(f"Selling {self.share_size} shares at {price} each for {total_sale_value} total.")
            else:
                print("Not enough shares to execute sell order.")

    def calculate_portfolio(self, data: pd.DataFrame) -> pd.Series:
        """
        Simulates portfolio growth based on strategy returns, ensuring portfolio value does not drop below zero.

        :param data: The backtest data containing strategy returns.
        :return: A pandas Series representing the portfolio value over time.
        """
        portfolio = []
        for index, row in data.iterrows():
            # Execute trade if there is a buy or sell signal
            if row['Position'] == 1:  # Buy signal
                self.execute_trade('buy', row['Close'])  # Simulate buying with the specified share size
            elif row['Position'] == -1:  # Sell signal
                self.execute_trade('sell', row['Close'])  # Simulate selling with the specified share size

            # Calculate portfolio value after trade
            portfolio_value = self.available_capital + self.shares_held * row['Close']
            portfolio.append(portfolio_value)

        return pd.Series(portfolio, index=data.index)  # Return the portfolio value series

class Strategy:
    """Strategy class for processing trading signals and executing trades."""

    def __init__(self, model: BaseModel, feature_columns: list):
        self.model = model
        self.feature_columns = feature_columns

    def generate_signals(self, data: pd.DataFrame):
        """Generate buy or sell signals based on the model's predictions."""
        signals = self.model.predict(data[self.feature_columns])
        return signals

    def execute_trades(self, executor: Executor, data: pd.DataFrame):
        """Executes trades based on generated signals."""
        signals = self.generate_signals(data)
        for idx, signal in enumerate(signals):
            price = data.iloc[idx]['Close']  # Assuming 'Close' is the price for the trade
            if signal == 1:  # Buy signal
                print(f"Signal: Buy at {price}")
                executor.execute_trade('buy', price)
            elif signal == -1:  # Sell signal
                print(f"Signal: Sell at {price}")
                executor.execute_trade('sell', price)

class RuleBasedStrategy:
    """A strategy for handling models that don't require fitting (e.g., agent-based or rule-based models)."""
    
    def __init__(self, model, feature_columns: list):
        """Initialize with a model and a list of feature columns."""
        self.model = model
        self.feature_columns = feature_columns

    def generate_signals(self, data: pd.DataFrame):
        """Generate buy or sell signals based on the model's predictions."""
        signals = self.model.predict(data[self.feature_columns])
        return signals

    def execute_trades(self, executor: Executor, data: pd.DataFrame):
        """Executes trades based on generated signals."""
        signals = self.generate_signals(data)
        for idx, signal in enumerate(signals):
            price = data.iloc[idx]['Close']
            if signal == 1:  # Buy signal
                print(f"Signal: Buy at {price}")
                executor.execute_trade('buy', price)
            elif signal == -1:  # Sell signal
                print(f"Signal: Sell at {price}")
                executor.execute_trade('sell', price)


class Backtester:
    """Framework for backtesting trading strategies with capital constraints and buy/sell logic."""

    def __init__(self, strategy: RuleBasedStrategy, executor: Executor, data: pd.DataFrame):
        self.strategy = strategy
        self.executor = executor
        self.data = data

    def run(self):
        """Executes the backtest, calculates performance metrics, and ensures capital constraints with buy/sell actions."""
        # Generate signals (1 for buy, -1 for sell, 0 for hold)
        self.data['Signal'] = self.strategy.generate_signals(self.data)
        self.data['Position'] = self.data['Signal'].shift(1)  # Use the previous signal

        # Calculate returns (this assumes daily returns)
        self.data['Daily_Return'] = self.data['Close'].pct_change()
        self.data['Strategy_Return'] = self.data['Position'] * self.data['Daily_Return']

        # Simulate portfolio growth with dynamic initial capital, capital tracking, and buy/sell actions
        self.data['Portfolio_Value'] = self.executor.calculate_portfolio(self.data)

        # Performance metrics
        final_portfolio_value = self.data['Portfolio_Value'].iloc[-1]
        total_return = (final_portfolio_value / self.executor.initial_capital) * 100

        # Calculate Sharpe ratio
        risk_free_rate = 4.75 / 100  # 4.75% annual risk-free rate
        daily_risk_free_rate = risk_free_rate / 252  # Convert to daily rate assuming 252 trading days

        # Calculate daily excess returns
        self.data['Excess_Return'] = self.data['Strategy_Return'] - daily_risk_free_rate

        # Sharpe ratio: mean of excess returns / standard deviation of excess returns
        sharpe_ratio = self.data['Excess_Return'].mean() / self.data['Excess_Return'].std()
        
        # Calculate cumulative portfolio value
        self.data['Cumulative_Portfolio'] = self.data['Portfolio_Value'].cummax()

        # Calculate drawdown
        self.data['Drawdown'] = (self.data['Portfolio_Value'] - self.data['Cumulative_Portfolio']) / self.data['Cumulative_Portfolio']

        # Maximum drawdown
        max_drawdown = self.data['Drawdown'].min()

        # Calculate downside deviation
        downside_deviation = self.data[self.data['Strategy_Return'] < daily_risk_free_rate]['Excess_Return'].std()

        # Sortino ratio
        sortino_ratio = self.data['Excess_Return'].mean() / downside_deviation

        # Calculate daily portfolio change
        self.data['Daily_Portfolio_Change'] = self.data['Portfolio_Value'].diff()

        # Calculate Win Rate
        # Create an array to track if each trade was a win or loss
        trade_results = []

        # Track portfolio value for the specific trades
        for idx in range(1, len(self.data)):
        # Look for buy (Signal == 1) and sell (Signal == -1) signals
            if self.data['Signal'].iloc[idx-1] == 1:  # Buy signal on previous day
                buy_price = self.data['Close'].iloc[idx]
            elif self.data['Signal'].iloc[idx-1] == -1:  # Sell signal on previous day
                sell_price = self.data['Close'].iloc[idx]
        
        # Calculate the change in portfolio value based on buy and sell prices
        if 'buy_price' in locals():
            profit_or_loss = sell_price - buy_price
            if profit_or_loss > 0:
                trade_results.append(1)  # Win
            else:
                trade_results.append(0)  # Loss
            del buy_price  # Reset buy_price for the next trade

        # Calculate Win Rate
        wins = sum(trade_results)
        total_trades = len(trade_results)
        win_rate = wins / total_trades * 100 if total_trades > 0 else 0
        
        # Calculate profits and losses
        gross_profit = self.data[self.data['Daily_Portfolio_Change'] > 0]['Daily_Portfolio_Change'].sum()
        gross_loss = abs(self.data[self.data['Daily_Portfolio_Change'] < 0]['Daily_Portfolio_Change'].sum())

        # Profit Factor
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')

        # Average Trade Return
        initial_value = self.data['Portfolio_Value'].iloc[0]
        final_value = self.data['Portfolio_Value'].iloc[-1]

        # Calculate average trade return
        average_trade_return = ((final_value - initial_value) / initial_value) * 100

        # Volatility
        volatility = self.data['Daily_Portfolio_Change'].std()

        # Calculate wins and losses
        winning_trades = self.data[self.data['Daily_Portfolio_Change'] > 0]
        losing_trades = self.data[self.data['Daily_Portfolio_Change'] < 0]

        # Average Win %
        average_win = (
        winning_trades['Daily_Portfolio_Change'].mean()  if not winning_trades.empty else 0
        )

        # Average Loss %
        average_loss = (
        losing_trades['Daily_Portfolio_Change'].mean()  if not losing_trades.empty else 0
        )


        metrics = {
            "Initial Portfolio Value": self.executor.initial_capital,
            "Final Portfolio Value": final_portfolio_value,
            "Total Return (%)": total_return,
            "Sharpe Ratio": sharpe_ratio,
            "Maximum Drawdown (%)": max_drawdown * 100,
            "Sortino Ratio": sortino_ratio,
            "Win Rate (%)": win_rate,
            "Profit Factor": profit_factor,
            "Average Trade Return (%)": average_trade_return,
            "Volatility (%)": volatility,
            "Average Win (%)": average_win,
            "Average Loss (%)": average_loss
        }

        return self.data[['Portfolio_Value']], metrics



def load_data(filepath, feature_columns=None):
    """Loads and preprocesses market data from a CSV file."""
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    if feature_columns is None:
        feature_columns = ['Close']

    df['Returns'] = df['Close'].pct_change()
    df.dropna(inplace=True)

    return df, feature_columns

def run_backtest(filepath, rule_based_model, feature_columns: list):
    """Runs a backtest for the specified rule-based model and data."""
    # Load data
    df, feature_columns = load_data(filepath, feature_columns)

    # Initialize RuleBasedStrategy (no need to call fit)
    strategy = RuleBasedStrategy(rule_based_model, feature_columns)
    executor = Executor()

    # Backtest
    backtester = Backtester(strategy, executor, df)
    portfolio_values, metrics = backtester.run()

    # Output metrics
    print("Backtest Results:")
    for key, value in metrics.items():
        print(f"{key}: {value:.2f}")

    return portfolio_values, metrics