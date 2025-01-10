
---

# Trading-Bot

## Algorithmic Trading Bot: Gap Up Strategy Backtesting and Live Deployment

### Overview
This project implements both a **backtesting framework** and a **live trading setup** for a **Gap Up Strategy** applied to Nifty 50 stocks. It uses historical data for backtesting and is designed for live deployment using Angel Broking's **SmartAPI**.

---

### Features
- **Backtesting:**
  - Fetches historical data for Nifty 50 stocks.
  - Implements a **Gap Up Strategy** with configurable parameters:
    - Gap percentage threshold.
    - Stop-loss percentage.
    - Risk-reward ratio.
    - Brokerage deduction.
  - Provides detailed trade logs and performance metrics.
  - Visualization of stock performance.

- **Live Trading:**
  - Monitors Nifty 50 stocks in real time.
  - Executes trades automatically based on the strategy parameters.
  - Dynamic token refresh for uninterrupted sessions.
  - Error handling and logging for live operations.

---

### Technologies Used
- **Python** for scripting.
- **Pandas** for data manipulation.
- **Matplotlib** for visualization.
- **SmartAPI** for data retrieval and order execution.
- **PyOTP** for API authentication.
- **Logzero** for logging in live deployment.

---

### How to Use

#### For Backtesting:
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Gap-Up-Trading-Bot.git
   ```
2. Install the required libraries:
   ```bash
   pip install pandas matplotlib pyotp logzero
   ```
3. Update your **API credentials** in the script:
   - `api_key`
   - `username`
   - `pwd`
   - `token` (for OTP generation).
4. Run the script:
   ```bash
   python script_name.py
   ```
5. Follow the prompts to specify the backtesting duration and view the results.

#### For Live Deployment:
1. Ensure your Angel Broking account is funded and active.
2. Update your API credentials in the script:
   - Add `SMART_API_KEY`, `SMART_API_USERNAME`, `SMART_API_PASSWORD`, and `SMART_API_TOTP_TOKEN` as environment variables.
3. Configure strategy parameters like:
   - Stop-loss percentage (`sl_pct`).
   - Risk-reward ratio (`rr_ratio`).
   - Gap percentage threshold.
   - Brokerage per trade.
4. Run the script in live mode:
   ```bash
   python script_name.py --live
   ```
5. Monitor trade logs in the `gap_up_strategy.log` file.

---

### Results
- **Backtesting Results:**
  - Summary of trades, profit and loss (PNL), and percentage returns.
  - Visualization of stock price movements and trades during the backtesting period.

- **Live Trading Results:**
  - Real-time trade logs.
  - PNL summary for live trades.
  - Error logs for troubleshooting.

---

### Notes
- Ensure your API credentials are valid before running the script.
- Modify the `get_nifty_50_tickers()` function to include the latest Nifty 50 tickers if required.
- Always test your strategy thoroughly in backtesting mode before deploying live.
- Use logging to monitor live performance and troubleshoot issues.

---

### Author
Adarsh Pal

---

### License
This project is open source and available under the [MIT License](LICENSE).

--- 

