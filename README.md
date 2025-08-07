# Fama-French 5-Factor Model Analysis

This repository contains a Python script for performing a Fama-French 5-Factor Model regression on individual stock returns. This project serves as a foundational exercise in quantitative finance, demonstrating the application of a widely-used asset pricing model.

## Project Goal

The primary goal of this script is to:
-   Acquire Fama-French 5-Factor data (Mkt-RF, SMB, HML, RMW, CMA, RF).
-   Download historical stock price data for a specified ticker.
-   Clean, preprocess, and merge the datasets, aligning their frequencies to monthly.
-   Run an Ordinary Least Squares (OLS) regression to estimate the stock's factor loadings (betas) and its alpha (idiosyncratic return).
-   Provide statistical summaries and basic residual analysis to evaluate model fit.

## Understanding the Fama-French 5-Factor Model

The Fama-French 5-Factor Model (F-F 5FM) is an asset pricing model that expands on the original 3-factor model by adding two new factors: Profitability (RMW) and Investment (CMA). It posits that a stock's expected return can be explained by its sensitivity to these five common risk factors:

1.  **Mkt-RF (Market Risk Premium):** The excess return of the market portfolio over the risk-free rate. This captures systematic market risk.
2.  **SMB (Small Minus Big):** The return of a portfolio of small-cap stocks minus the return of a portfolio of large-cap stocks. This captures the size premium.
3.  **HML (High Minus Low):** The return of a portfolio of high book-to-market (value) stocks minus the return of a portfolio of low book-to-market (growth) stocks. This captures the value premium.
4.  **RMW (Robust Minus Weak):** The return of a portfolio of high operating profitability stocks minus the return of a portfolio of low operating profitability stocks. This captures the profitability premium.
5.  **CMA (Conservative Minus Aggressive):** The return of a portfolio of low investment stocks (conservative) minus the return of a portfolio of high investment stocks (aggressive). This captures the investment premium.
6.  **RF (Risk-Free Rate):** The return on a one-month U.S. Treasury Bill.

The regression equation is typically:
$R_i - R_f = \alpha_i + \beta_{Mkt}(R_M - R_f) + \beta_{SMB}SMB + \beta_{HML}HML + \beta_{RMW}RMW + \beta_{CMA}CMA + \epsilon_i$

Where:
-   $R_i$: Return of the asset
-   $R_f$: Risk-free rate
-   $R_M$: Return of the market portfolio
-   $\alpha_i$: Alpha (intercept), representing the asset's idiosyncratic return
-   $\beta$: Factor loadings (sensitivities) to each factor
-   $\epsilon_i$: Error term

## Data Sources

-   **Fama-French 5-Factor Data:** The `F-F_Research_Data_5_Factors_2x3.csv` file is a local copy of the Fama-French 5-Factor data, which is based on the **U.S. market**. This data is typically obtained from Kenneth R. French's data library (e.g., from his Dartmouth website).
-   **Stock Price Data:** Fetched using the `yfinance` library, which provides historical stock data from Yahoo Finance.

## How to Run

1.  **Ensure Dependencies:** Make sure you have the necessary Python libraries installed. It's recommended to use a virtual environment.
    ```bash
    pip install pandas numpy statsmodels yfinance seaborn matplotlib
    ```
2.  **Place Factor Data:** Ensure the `F-F_Research_Data_5_Factors_2x3.csv` file is located in the same directory as `factor_model.py`.
3.  **Execute the Script:** Run the `factor_model.py` script. The `ticker` variable is currently hardcoded to `'AAPL'` for demonstration purposes. You can modify this variable within the script to analyze other U.S. stock tickers.
    ```bash
    python factor_model.py
    ```

## Interpretation of Regression Results

The script outputs a detailed OLS regression summary from `statsmodels`. Key elements to interpret include:

-   **`Dep. Variable: y`**: This is the excess return of the stock ($R_i - R_f$).
-   **`R-squared`**: Indicates the proportion of the variance in the stock's excess returns that is explained by the five factors. A higher R-squared means the model explains more of the stock's movements.
-   **`const` (Alpha, $\alpha_i$)**: 
    -   **`coef`**: The estimated alpha value. A positive alpha suggests the stock has outperformed its expected return given its factor exposures.
    -   **`P>|z|`**: The p-value for the alpha coefficient. A p-value less than 0.05 (or 0.01, depending on significance level) indicates that the alpha is statistically significant and likely not due to random chance.
-   **Factor Coefficients ($\beta$s)**:
    -   **`coef`**: The estimated sensitivity of the stock's excess returns to each factor. For example, a `Mkt-RF` coefficient of 1.2 means the stock tends to move 1.2% for every 1% move in the market excess return.
    -   **`P>|z|`**: The p-value for each factor coefficient. A low p-value indicates that the stock's exposure to that factor is statistically significant.
-   **Residual Analysis**:
    -   The script generates plots of residuals over time and their distribution. These are crucial for checking the assumptions of OLS regression (e.g., homoscedasticity, normality of residuals). Deviations can indicate issues with the model or missing factors.

## Limitations and Future Work

This project provides a solid foundation but has several areas for expansion:

### Current Limitations:
-   **Pre-computed Factors:** This project uses pre-computed Fama-French factors. A full replication would involve constructing these factors from raw stock data (requiring comprehensive historical stock characteristics like market equity and book value, and careful portfolio formation rules). This is a significant data challenge for personal projects without access to institutional databases like CRSP and Compustat.
-   **U.S. Market Focus:** The factors used are for the U.S. market. Applying this directly to non-U.S. stocks (e.g., Indian stocks) is inappropriate without corresponding local market factors.
-   **Survivorship Bias:** The current stock data acquisition from `yfinance` might suffer from survivorship bias (only including currently listed companies), which can distort historical analysis.
-   **Simple Data Handling:** The script assumes the Fama-French CSV format is consistent. More robust data pipelines would include error handling for unexpected file formats or missing data.

### Potential Future Work:
-   **Factor Construction:** Implement the logic to construct SMB, HML, RMW, and CMA factors from a comprehensive universe of raw stock data (if suitable data can be acquired).
-   **International Factors:** Extend the analysis to other markets by sourcing or constructing international Fama-French factors.
-   **Time-Varying Betas:** Explore models where factor sensitivities ($\beta$s) are not constant but change over time (e.g., using Kalman filters or rolling regressions).
-   **Other Factor Models:** Implement and compare other factor models (e.g., Carhart 4-Factor, AQR's Quality-Minus-Junk, Betting-Against-Beta).
-   **Portfolio Analysis:** Integrate this analysis into a broader portfolio context, examining how factor exposures contribute to portfolio risk and return.
-   **Automated Data Fetching:** Implement direct fetching of Fama-French data from Ken French's website within the script, removing the need for a local CSV.