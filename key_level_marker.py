import datetime
from typing import List, Tuple

import matplotlib
import matplotlib.dates as dates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
from mplfinance.original_flavor import _candlestick

matplotlib.use("agg")

# Plot Settings
plt.rcParams["figure.figsize"] = [10, 6]
plt.rc("font", size=14)


def getTickerInformation(
    ticker_symbol: str,
    interval: str,
    start: str,
    end: str = datetime.date.today().strftime("%Y-%m-%d"),
) -> pd.DataFrame:
    ticker = yf.Ticker(ticker_symbol)
    df = ticker.history(interval=interval, start=start, end=end)
    df["Date"] = pd.to_datetime(df.index)
    df["Date"] = df["Date"].apply(dates.date2num)
    df = df.loc[:, ["Date", "Open", "High", "Low", "Close"]]
    return df


def isSupport(df: pd.DataFrame, i: int) -> bool:
    cond1 = df["Low"][i] < df["Low"][i - 1]
    cond2 = df["Low"][i] < df["Low"][i + 1]
    cond3 = df["Low"][i + 1] < df["Low"][i + 2]
    cond4 = df["Low"][i + 1] < df["Low"][i + 2]
    support = cond1 and cond2 and cond3 and cond4
    return support


def isResistance(df: pd.DataFrame, i: int) -> bool:
    cond1 = df["High"][i] > df["High"][i - 1]
    cond2 = df["High"][i] > df["High"][i + 1]
    cond3 = df["High"][i + 1] > df["High"][i + 2]
    cond4 = df["High"][i - 1] > df["High"][i - 2]
    resistance = cond1 and cond2 and cond3 and cond4
    return resistance


def isFarFromLevel(df: pd.DataFrame, levels: List[float], level: float):
    s = np.mean(df["High"] - df["Low"])
    return np.sum([abs(level - x) < s for x in levels]) == 0


def calculateKeyLevels(df: pd.DataFrame) -> List[Tuple]:
    levels = []
    for i in range(2, df.shape[0] - 2):
        if isSupport(df, i):
            level = df["Low"][i]
            print(i, level)
            if isFarFromLevel(df, levels.copy(), level):
                levels.append((i, level))
        elif isResistance(df, i):
            level = df["High"][i]
            print(i, level)
            if isFarFromLevel(df, levels.copy(), level):
                levels.append((i, level))
    return levels


def plot_all(df: pd.DataFrame) -> str:
    fig, ax = plt.subplots()
    _candlestick(ax, df.values, 0.6, "green", "red", 0.8)
    date_format = dates.DateFormatter("%d %b %Y")
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()
    fig.tight_layout()
    levels = calculateKeyLevels(df)
    for level in levels:
        plt.hlines(level[1], df["Date"][level[0]], max(df["Date"]), "blue")
    plot_path = "static/charts/candlestick_plot.png"
    plt.savefig(plot_path)

    # Close the figure to free up memory
    plt.close(fig)

    print(f"Plot saved to {plot_path}")

    return plot_path
