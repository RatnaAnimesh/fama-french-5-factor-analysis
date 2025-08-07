# Fama-French 5-Factor Model Analysis

This repository contains a Python script for performing a Fama-French 5-Factor Model regression on individual stock returns. The model aims to explain a stock's excess returns based on its exposure to market, size, value, profitability, and investment factors.

## Project Goal

The primary goal of this script is to:
- Acquire Fama-French 5-Factor data.
- Download historical stock price data for a specified ticker.
- Merge the datasets and align their frequencies.
- Run an Ordinary Least Squares (OLS) regression to estimate the stock's factor loadings (betas) and its alpha (idiosyncratic return).
- Provide statistical summaries and residual analysis.

## Data Sources

- **Fama-French 5-Factor Data:** The `F-F_Research_Data_5_Factors_2x3.csv` file is a local copy of the Fama-French 5-Factor data, which is based on the **U.S. market**. This data is typically obtained from Kenneth R. French's data library.
- **Stock Price Data:** Fetched using the `yfinance` library, which provides historical stock data from Yahoo Finance.

## How to Run

1.  **Ensure Dependencies:** Make sure you have the necessary Python libraries installed: `pandas`, `numpy`, `statsmodels`, `yfinance`, `seaborn`, `matplotlib`. You can install them via pip:
    ```bash
    pip install pandas numpy statsmodels yfinance seaborn matplotlib
    ```
2.  **Place Factor Data:** Ensure the `F-F_Research_Data_5_Factors_2x3.csv` file is located in the same directory as `factor_model.py`.
3.  **Execute the Script:** Run the `factor_model.py` script. The script is currently configured to analyze 'AAPL' (Apple Inc.). You can modify the `ticker` variable within the script to analyze other U.S. stocks.
    ```bash
    python factor_model.py
    ```

## Interpretation of Results

The output will include:
- Descriptive statistics and correlation matrix of the factors.
- A detailed OLS regression summary, showing:
    - **Alpha (const coefficient):** The stock's excess return not explained by the factors. A positive and statistically significant alpha suggests outperformance.
    - **Factor Betas:** The sensitivity of the stock's returns to each of the five factors (Mkt-RF, SMB, HML, RMW, CMA).
    - **R-squared:** The proportion of the stock's return variance explained by the factors.
- Plots of residuals over time and their distribution, which are important for checking model assumptions.

## Note on Factor Construction

This project utilizes pre-computed Fama-French factors. A more advanced extension would involve constructing these factors from raw stock data (requiring comprehensive historical stock characteristics and careful portfolio formation rules).
