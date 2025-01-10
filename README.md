# Trading-Bot.


# Algorithmic Trading Bot: Gap Up Strategy Backtesting

## Overview
This project implements a backtesting framework for a **Gap Up Strategy** applied to Nifty 50 stocks. It uses historical data to evaluate the strategy's profitability and provides detailed trade logs and performance metrics.

## Features
- Fetches historical data for Nifty 50 stocks using Angel Broking's **SmartAPI**.
- Implements a **Gap Up Strategy** with configurable parameters:
  - Gap percentage threshold
  - Stop-loss percentage
  - Risk-reward ratio
  - Brokerage deduction
- Detailed profit and loss (PNL) calculations.
- Visualization of stock performance during the backtesting period.

## Technologies Used
- **Python** for scripting
- **Pandas** for data manipulation
- **Matplotlib** for visualization
- **SmartAPI** for data retrieval
- **PyOTP** for API authentication

## How to Use
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
   - `token` (for OTP generation)
4. Run the script:
   ```bash
   python script_name.py
   ```
5. Follow the prompts to specify the backtesting duration and view the results.

## Results
- The bot provides a summary of all trades, profit and loss (PNL), and percentage returns for the specified duration.
- Visualization of stock price movements and trades during the backtesting period.

## Notes
- Ensure your API credentials are valid before running the script.
- Modify the `get_nifty_50_tickers()` function to include the latest Nifty 50 tickers if required.
- The script supports configurable parameters for easy customization of trading strategy.

## Author
Adarsh Pal

## License
This project is open source and available under the [MIT License](LICENSE).
```

Update the GitHub repository URL and script name in the `README.md` before uploading!
