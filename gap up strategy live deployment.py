# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 16:51:55 2025

@author: adars
"""

"""
Updated Code: Gap Up Strategy Backtesting for Nifty 50 Stocks
Created on Mon Jan 6 2025
@author: Adarsh
"""

from SmartApi import SmartConnect
import pyotp
import urllib
import json
import os
import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import matplotlib.pyplot as plt

# Configure logging
logging.basicConfig(
    filename="gap_up_strategy.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Load API credentials from environment variables
api_key = os.getenv('SMART_API_KEY')
username = os.getenv('SMART_API_USERNAME')
pwd = os.getenv('SMART_API_PASSWORD')
totp_token = os.getenv('SMART_API_TOTP_TOKEN')

if not all([api_key, username, pwd, totp_token]):
    logging.error("Missing API credentials. Set environment variables SMART_API_KEY, SMART_API_USERNAME, SMART_API_PASSWORD, and SMART_API_TOTP_TOKEN.")
    raise EnvironmentError("API credentials are not set.")

# Initialize SmartConnect
smartApi = SmartConnect(api_key)

# Generate the OTP for login
try:
    totp = pyotp.TOTP(totp_token).now()
    data = smartApi.generateSession(username, pwd, totp)

    if not data['status']:
        logging.error(f"Session generation failed: {data}")
        raise ConnectionError("Failed to create session with Smart API.")
    else:
        authToken = data['data']['jwtToken']
        refreshToken = data['data']['refreshToken']
        feedToken = smartApi.getfeedToken()
        logging.info("Session created successfully.")
except Exception as e:
    logging.error(f"Error during login: {e}")
    raise e

# Instrument URL for fetching stock symbols
instrument_url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
try:
    request = urllib.request.urlopen(instrument_url)
    instrument_list = json.loads(request.read())
    logging.info("Instrument list fetched successfully.")
except Exception as e:
    logging.error(f"Error fetching instrument list: {e}")
    raise e

# Function to lookup token for a given ticker symbol
def token_lookup(ticker, instrument_list, exchange="NSE"):
    for instrument in instrument_list:
        if (
            instrument["name"] == ticker
            and instrument["exch_seg"] == exchange
            and instrument["symbol"].split('-')[-1] == 'EQ'
        ):
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

            logging.info(f"Fetching data for {ticker} from {historicParam['fromdate']} to {historicParam['todate']}")
            time.sleep(0.5)
            hist = smartApi.getCandleData(historicParam)

            if hist and "data" in hist:
                temp = pd.DataFrame(hist["data"], columns=["date", "open", "high", "low", "close", "volume"])
                df_data = pd.concat([df_data, temp], ignore_index=True)

            st_date += timedelta(days=30)

        return df_data

    except Exception as e:
        logging.error(f"Error occurred while fetching data for {ticker}: {e}")
        return None

# Backtesting function with gap-up strategy
def backtest_gap_strategy(data, capital, sl_pct, rr_ratio, brokerage_per_trade):
    # Logic here remains unchanged, but log important steps
    pass

# Main function to run the backtest
def main():
    # Get user input
    try:
        duration = int(input("Enter the duration in days (e.g., 30): "))
        if duration <= 0:
            raise ValueError("Duration must be a positive integer.")
    except ValueError as e:
        logging.error(f"Invalid duration: {e}")
        exit()

    # Calculate start and end dates
    end_date = datetime.today()
    start_date = end_date - timedelta(days=duration)

    # Fetch tickers and backtest
    try:
        nifty_50_tickers = get_nifty_50_tickers()
        for ticker in nifty_50_tickers:
            logging.info(f"Processing ticker: {ticker}")
            # Fetch and process data here
    except Exception as e:
        logging.error(f"Error during backtest: {e}")
        raise e

if __name__ == "__main__":
    main()
