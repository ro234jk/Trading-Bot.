# -*- coding: utf-8 -*- 
"""
Updated Code: Gap Up Strategy Backtesting for Nifty 50 Stocks
Created on Mon Jan 6 2025
@author: Adarsh
"""

from SmartApi import SmartConnect
import pyotp
import urllib
import json
from logzero import logger
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import matplotlib.pyplot as plt
import os

# Instrument URL for fetching stock symbols
instrument_url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
request = urllib.request.urlopen(instrument_url)
instrument_list = json.loads(request.read())

# API credentials
api_key = '1GqCalA6'
username = 'AAAD602507'
pwd = '2209'

# Initialize SmartConnect
smartApi = SmartConnect(api_key)

# Generate the OTP for login
try:
    token = "E4LEKLXIJM3SHH2ARQS2UT6NQE"
    totp = pyotp.TOTP(token).now()
except Exception as e:
    logger.error("Invalid Token: The provided token is not valid.")
    raise e

# Create session
data = smartApi.generateSession(username, pwd, totp)

if data['status'] == False:
    logger.error(data)
else:
    authToken = data['data']['jwtToken']
    refreshToken = data['data']['refreshToken']
    feedToken = smartApi.getfeedToken()
    res = smartApi.getProfile(refreshToken)
    smartApi.generateToken(refreshToken)

# Function to lookup token for a given ticker symbol
def token_lookup(ticker, instrument_list, exchange="NSE"):
    for instrument in instrument_list:
        if instrument["name"] == ticker and instrument["exch_seg"] == exchange and instrument["symbol"].split('-')[-1] == 'EQ':
            return instrument["token"]
    return None

# Function to fetch historical data
def fetch_historic_data(smartApi, st_date, end_date, ticker, instrument_list):
    try:
        df_data = pd.DataFrame()
        while st_date < end_date:
            historicParam = {
                "exchange": "NSE",
                "symboltoken": token_lookup(ticker, instrument_list),
                "interval": "FIVE_MINUTE",
                "fromdate": st_date.strftime("%Y-%m-%d %H:%M"),
                "todate": (st_date + timedelta(days=30)).strftime("%Y-%m-%d %H:%M")
            }
            if datetime.strptime(historicParam['todate'], "%Y-%m-%d %H:%M") > end_date:
                historicParam["todate"] = end_date.strftime("%Y-%m-%d %H:%M")

            print(f"Fetching data from {historicParam['fromdate']} to {historicParam['todate']}")
            time.sleep(0.5)
            hist = smartApi.getCandleData(historicParam)

            if hist and "data" in hist:
                temp = pd.DataFrame(hist["data"], columns=["date", "open", "high", "low", "close", "volume"])
                df_data = pd.concat([df_data, temp], ignore_index=True)

            st_date += timedelta(days=30)

        return df_data

    except Exception as e:
        print(f"Error occurred: {e}")
        return None

# Backtesting function with gap up strategy for Nifty 50 stocks
def backtest_gap_strategy(data, capital, sl_pct, rr_ratio, brokerage_per_trade):
    # Calculate returns (percentage change from open to close)
    data['returns'] = (data['close'] - data['open']) / data['open'] * 100
    gap_up = data[data['returns'] >= 2]  # Filter for gap up more than or equal to 2%

    trades = []  # To store trade details
    pnl = 0
    position = "None"
    entry_price = 0
    stop_loss = 0
    target = 0

    for i in range(1, len(data)):
        # Implementing gap-up strategy
        if gap_up['returns'].iloc[i] >= 2 and position == "None":
            if data['close'].iloc[i] > data['open'].iloc[i-1]:  # Check if price breaks 9:25 AM level
                position = "Long"
                entry_price = data['close'].iloc[i]
                stop_loss = entry_price * (1 - sl_pct / 100)
                target = entry_price * (1 + (sl_pct * rr_ratio) / 100)
                trades.append(f"Entered Long at {entry_price}")
                
        elif position == "Long":
            if data['close'].iloc[i] <= stop_loss or data['close'].iloc[i] >= target:
                exit_price = data['close'].iloc[i]
                pnl += (exit_price - entry_price) if exit_price >= target else (entry_price - exit_price)
                pnl -= brokerage_per_trade  # Deduct brokerage for each trade
                trades.append(f"Exited Long at {exit_price}")
                position = "None"

    return {
        "PNL": pnl,
        "Trades": trades
    }

# Plot results
def plot_results(data, trades):
    plt.figure(figsize=(14, 7))
    plt.plot(data.index, data['close'], label='Close Price', alpha=0.7)
    plt.title('Gap Up Strategy Backtest for Nifty 50 Stocks')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()
    plt.show()

# Function to get Nifty 50 stocks
def get_nifty_50_tickers():
    # You can manually define or pull the latest Nifty 50 list from any source
    return ['TCS', 'INFY', 'WIPRO', 'HDFCBANK', 'RELIANCE', 'KOTAKBANK', 'ICICIBANK', 'LT', 'HDFC', 'SBIN', 'BAJAJ-FINANCE', 'ITC', 'MARUTI', 'TATAMOTORS', 'M&M', 'HUL', 'ASIANPAINT', 'HDFC-LIFE', 'NTPC', 'ONGC', 'SUNPHARMA', 'POWERGRID', 'TITAN', 'ULTRACEMCO', 'CIPLA', 'HCLTECH', 'BAJAJ-AUTO', 'DIVISLAB', 'DRREDDY', 'BHARTIARTL', 'INDUSINDBK', 'ADANIGREEN', 'ADANIPORTS', 'HEROMOTOCO', 'HDFCAMC', 'SHREECEM', 'BPCL', 'COALINDIA', 'GAIL', 'MCDOWELL-N', 'AUROPHARMA', 'TATACONSUM', 'ITC', 'UPL']

# Main function to run backtest for the specified number of days
def main():
    # Get user input for the number of days
    try:
        duration = int(input("Enter the duration in days (e.g., 30): "))
        if duration <= 0:
            raise ValueError("Duration must be a positive integer.")
    except ValueError as e:
        print(f"Invalid duration: {e}")
        exit()

    # Calculate start and end dates
    end_date = datetime.today()
    start_date = end_date - timedelta(days=duration)

    # Get Nifty 50 tickers
    nifty_50_tickers = get_nifty_50_tickers()

    all_trades = []
    all_pnl = 0

    for ticker in nifty_50_tickers:
        print(f"Fetching data for {ticker}...")
        df_data = fetch_historic_data(smartApi, start_date, end_date, ticker, instrument_list)

        if df_data is not None and not df_data.empty:
            df_data.set_index("date", inplace=True)
            df_data.index = pd.to_datetime(df_data.index)
            df_data.index = df_data.index.tz_localize(None)

            performance = backtest_gap_strategy(df_data, capital=100000, sl_pct=1, rr_ratio=2, brokerage_per_trade=20)

            if performance:
                print(f"Performance for {ticker}:")
                for metric, value in performance.items():
                    if isinstance(value, list):
                        for trade in value:
                            print(trade)
                    else:
                        print(f"{metric}: {value}")

                # Calculate and display profit percentage
                initial_capital = 100000
                profit_percentage = (performance["PNL"] / initial_capital) * 100
                print(f"Profit Percentage for {ticker}: {profit_percentage:.2f}%")

                all_trades.extend(performance["Trades"])
                all_pnl += performance["PNL"]

    print(f"\nTotal PNL from all trades: {all_pnl}")
    print(f"Total Profit Percentage: {(all_pnl / 100000) * 100:.2f}%")

    # Optionally plot results (you can modify this to include a summary of all tickers)
    # plot_results(df_data, all_trades)

if __name__ == "__main__":
    main()
