import pandas as pd
import numpy as np
import statsmodels.api as sm
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt

# Check if yfinance is installed
try:
    import yfinance as yf
except ImportError:
    print("Error: yfinance is not installed. Please install it using 'pip install yfinance'")
    exit()

# Check if seaborn is installed
try:
    import seaborn as sns
    import matplotlib.pyplot as plt
except ImportError:
    print("Error: seaborn or matplotlib is not installed. Please install them using 'pip install seaborn matplotlib'")
    exit()


# Define the path to your data file
file_path = '/Users/ashishmishra/fama-french/F-F_Research_Data_5_Factors_2x3.csv'

# Load the data
try:
    # The Fama-French data has a few header rows before the actual data
    df = pd.read_csv(file_path, skiprows=3, skipfooter=65, engine='python')
    print("Data loaded successfully.")
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
    exit()

# Data Preprocessing
# Rename the first column to 'Date'
df = df.rename(columns={df.columns[0]: 'Date'})
# Convert 'Date' column to datetime objects
# The format is YYYYMM, so we need to convert it to a proper date format
df['Date'] = pd.to_datetime(df['Date'], format='%Y%m')
# Divide factor values by 100 to convert from percentage to decimal
for col in ['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA', 'RF']:
    df[col] = df[col] / 100

# Replace 'NA' with NaN and convert relevant columns to numeric
# Assuming SMB, HML, WML, MF, RF are the factor columns
factor_columns = ['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA', 'RF']
# No resampling needed as the data is already monthly

print("\nFirst 5 rows of the preprocessed monthly factor data:")
print(df.head())

print("\nData types after preprocessing (monthly factors):")
print(df.dtypes)

print("\nMissing values after preprocessing (monthly factors):")
print(df.isnull().sum())

# Exploratory Data Analysis (EDA)
print("\nDescriptive Statistics:")
print(df[factor_columns].describe())

print("\nCorrelation Matrix:")
print(df[factor_columns].corr())

# # Acquire Asset Returns (AAPL)
print("\nAcquiring stock data...")
# Define the ticker and date range (align with factor data)
# The factor data starts from 1993-10-01, so we'll use a similar range.
start_date = df['Date'].min()
end_date = df['Date'].max()

ticker = 'AAPL'
stock_data = yf.download(ticker, start=start_date, end=end_date, progress=False)

# Calculate monthly returns for the stock
monthly_prices = stock_data['Close'].resample('ME').last()
monthly_returns = monthly_prices.pct_change()
stock_data_monthly = pd.DataFrame(monthly_returns)
stock_data_monthly.columns = ['Stock_Returns']
stock_data_monthly.reset_index(inplace=True)

# Ensure 'Date' column in both dataframes are consistent for merging
df['Date'] = df['Date'].dt.to_period('M').dt.to_timestamp('M')
stock_data_monthly['Date'] = stock_data_monthly['Date'].dt.to_period('M').dt.to_timestamp('M')

# Merge stock returns with the factor data
df_merged = pd.merge(df, stock_data_monthly, on='Date', how='inner')

print("\nFirst 5 rows of merged data with AAPL Returns:")
print(df_merged.head())

print("\nMissing values after merging:")
print(df_merged.isnull().sum())

# Drop rows with any missing values for the regression analysis
df_merged.dropna(inplace=True)

print("\nShape of data after dropping missing values:", df_merged.shape)

# Generate pairplot using seaborn
print("\nGenerating pairplot...")
sns.pairplot(df_merged[factor_columns + ['Stock_Returns']])
plt.suptitle('Pairplot of Factors and Stock Returns', y=1.02) # Add a title
plt.show()

# Factor Model Construction (OLS Regression)

print("\nBuilding Factor Model...")

# Define dependent variable (Y) and independent variables (X)
df_merged['Market_Excess_Returns'] = df_merged['Mkt-RF']

# Define dependent variable (Y) and independent variables (X)
Y = df_merged['Stock_Returns'] - df_merged['RF']
X = df_merged[['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']] # Using all five factors

# Add a constant to the independent variables for the intercept (alpha)
X = sm.add_constant(X)

# Fit the OLS model
model = sm.OLS(Y, X)
results = model.fit(cov_type='HC3')

# Model Evaluation
print("\nFactor Model Regression Results:")
print(results.summary())

# --- Residual Analysis ---
print("\nAnalyzing Residuals...")

# 1. Residuals Time Series Plot
plt.figure(figsize=(12, 6))
plt.plot(df_merged['Date'], results.resid, label='Residuals')
plt.axhline(0, color='red', linestyle='--', linewidth=0.8)
plt.title('Residuals Over Time')
plt.xlabel('Date')
plt.ylabel('Residuals')
plt.grid(True)
plt.legend()
plt.show()

# 2. Residuals Histogram
plt.figure(figsize=(8, 6))
sns.histplot(results.resid, kde=True)
plt.title('Distribution of Residuals')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.show()









