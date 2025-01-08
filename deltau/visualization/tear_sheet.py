import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class TearSheet:
    def __init__(self, backtest_results: pd.DataFrame, metrics: dict):
        """
        Initialize the TearSheet with backtest results and performance metrics.

        :param backtest_results: DataFrame with 'Date' and 'Portfolio_Value'.
        :param metrics: Dictionary containing performance metrics.
        """
        self.backtest_results = backtest_results
        self.metrics = metrics

    def generate_report(self):
        """
        Generate a summary of performance metrics.

        :return: Performance metrics as a DataFrame.
        """
        metrics_df = pd.DataFrame(self.metrics.items(), columns=["Metric", "Value"])
        return metrics_df

    def plot_equity_curve(self):
        """
        Plot the equity curve using Plotly.

        :return: Plotly figure object for the equity curve.
        """
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=self.backtest_results.index,
            y=self.backtest_results['Portfolio_Value'],
            mode='lines',
            name='Equity Curve'
        ))

        fig.update_layout(
            title="Equity Curve",
            xaxis_title="Date",
            yaxis_title="Portfolio Value",
            template="plotly_white"
        )

        return fig

    def plot_drawdown(self):
        """
        Plot the drawdown curve using Plotly.

        :return: Plotly figure object for the drawdown curve.
        """
        portfolio_values = self.backtest_results['Portfolio_Value']
        rolling_max = portfolio_values.cummax()
        drawdown = (portfolio_values - rolling_max) / rolling_max

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=self.backtest_results.index,
            y=drawdown,
            mode='lines',
            name='Drawdown'
        ))

        fig.update_layout(
            title="Drawdown Curve",
            xaxis_title="Date",
            yaxis_title="Drawdown",
            template="plotly_white"
        )

        return fig

    def plot_win_rate(self):
        """
        Plot the win rate as a bar chart using Plotly.

        :return: Plotly figure object for the win rate.
        """
        # Use the pre-calculated Win Rate from the metrics dictionary
        win_rate = self.metrics.get("Win Rate (%)", 0)

        fig = go.Figure()

        fig.add_trace(go.Bar(
        x=["Win Rate"],
        y=[win_rate],
        text=[f"{win_rate:.2f}%"],
        textposition='outside',
        name="Win Rate"
        ))

        fig.update_layout(
        title="Win Rate",
        xaxis_title="Metric",
        yaxis_title="Percentage",
        yaxis=dict(range=[0, 100]),  # Limit y-axis to 0-100%
        template="plotly_white"
        )

        return fig


    def plot_average_loss(self):
        """
        Plot the average loss as a bar chart using Plotly.

        :return: Plotly figure object for the average loss.
        """
        # Use the pre-calculated Average Loss from the metrics dictionary
        average_loss = self.metrics.get("Average Loss (%)", 0)

        fig = go.Figure()

        fig.add_trace(go.Bar(
        x=["Average Loss"],
        y=[average_loss],
        text=[f"{average_loss:.2f}%"],
        textposition='outside',
        name="Average Loss"
        ))

        fig.update_layout(
        title="Average Loss",
        xaxis_title="Metric",
        yaxis_title="Percentage",
        template="plotly_white"
        )

        return fig

    def plot_performance_summary(self):
        """
        Plot a combined performance summary with the equity and drawdown curves.

        :return: Plotly figure object with subplots for equity and drawdown curves.
        """
        portfolio_values = self.backtest_results['Portfolio_Value']
        rolling_max = portfolio_values.cummax()
        drawdown = (portfolio_values - rolling_max) / rolling_max

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                            subplot_titles=("Equity Curve", "Drawdown Curve"))

        # Equity Curve
        fig.add_trace(go.Scatter(
            x=self.backtest_results.index,
            y=portfolio_values,
            mode='lines',
            name='Equity Curve'
        ), row=1, col=1)

        # Drawdown Curve
        fig.add_trace(go.Scatter(
            x=self.backtest_results.index,
            y=drawdown,
            mode='lines',
            name='Drawdown'
        ), row=2, col=1)

        fig.update_layout(
            title="Performance Summary",
            template="plotly_white",
            height=800
        )

        fig.update_xaxes(title_text="Date", row=2, col=1)
        fig.update_yaxes(title_text="Portfolio Value", row=1, col=1)
        fig.update_yaxes(title_text="Drawdown", row=2, col=1)

        return fig

    def display_report(self):
        """
        Display the report, including metrics and plots.

        :return: None.
        """
        # Display metrics
        metrics_df = self.generate_report()
        print("Performance Metrics:\n", metrics_df.to_string(index=False))

        # Display plots
        equity_curve_fig = self.plot_equity_curve()
        drawdown_fig = self.plot_drawdown()
        performance_summary_fig = self.plot_performance_summary()
        win_rate_fig = self.plot_win_rate()
        average_loss_fig = self.plot_average_loss()
        ##
        equity_curve_fig.show()
        drawdown_fig.show()
        performance_summary_fig.show()
        win_rate_fig.show()
        average_loss_fig.show()
