# This file is part of the Python Projects repository, which is licensed under the
# Apache License, Version 2.0. You may obtain a copy of the license at
#
#     http://www.apache.org/licenses/LICENSE-2.0

"""
Rainy Days Count in a Year Program.

Input:
- CSV file.

Output:
- Displays a histogram of rainfall and provides statistics on rainy days.

Features:
- Load and preprocess CSV data.
- Plot a histogram of rainfall distribution.
- Analyze and print statistics on rainy days.
- Plot monthly average rainfall.
- Analyze and visualize rainfall patterns across different seasons.
- Categorize rainfall into light, moderate, and heavy rain.
- Explore trends or patterns in rainfall over the course of the year.
- Identify and analyze extreme rainfall events or outliers.
- Explore correlations between rainfall and other meteorological factors.
- Create an interactive rainfall visualization using Plotly Express.
- Explore machine learning models for predicting future rainfall based on historical data.

"""

import numpy as np
import pandas as pd
import warnings
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from scipy.stats import linregress, zscore
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

def load_data(file_path):
   """Load and preprocess the CSV data."""

   data = pd.read_csv(file_path)
   data['DATE'] = pd.to_datetime(data['DATE'], format='%Y%m%d')
   return data

def plot_rainfall_histogram(inches):
   """Plot a histogram of rainfall."""

   sns.set()
   plt.figure(figsize=(12, 8))

   # Plot histogram
   sns.histplot(inches, bins=30, kde=True, color='skyblue', edgecolor='w', linewidth=1.2)

   # Add title and labels
   plt.title("Distribution of Rainfall in Seattle (2014)", fontsize=16)
   plt.xlabel("Rainfall (inches)", fontsize=14)
   plt.ylabel("Frequency", fontsize=14)

   # Add mean and median lines
   mean_rainfall = np.mean(inches)
   median_rainfall = np.median(inches)
   plt.axvline(mean_rainfall, color='orange', linestyle='dashed', linewidth=2, label=f'Mean: {mean_rainfall:.2f}')
   plt.axvline(median_rainfall, color='green', linestyle='dashed', linewidth=2, label=f'Median: {median_rainfall:.2f}')

   # Add legend
   plt.legend()
   plt.show()

def analyze_rainy_days(inches):
   """Analyze rainy days and print statistics."""

   rainy_days = inches[inches > 0]
   print(f"Number of days without rain: {np.sum(inches == 0)}")
   print(f"Number of days with rain: {len(rainy_days)}")
   print(f"Number of days with rain more than 0.5 inches: {np.sum(inches > 0.5)}")
   print(f"Number of days with rain < 0.2 inches: {np.sum((inches > 0) & (inches < 0.2))}")

def plot_monthly_average(data):
   """Calculate and plot the monthly average rainfall."""

   data.set_index('DATE', inplace=True)
   monthly_average = data['PRCP'].resample('ME').mean()
   
   sns.set()
   plt.figure(figsize=(12, 8))
   sns.barplot(x=monthly_average.index.month_name(), y=monthly_average, hue=monthly_average.index.month_name(), palette='Blues', legend=False)
   plt.title("Monthly Average Rainfall in Seattle (2014)")
   plt.xlabel("Month")
   plt.ylabel("Average Rainfall (inches)")
   plt.show()

def plot_seasonal_analysis(data):
   """Analyze and visualize rainfall patterns across different seasons."""

   data['Season'] = pd.cut(data.index.month,
                           bins=[0, 3, 6, 9, 12],
                           labels=['Winter', 'Spring', 'Summer', 'Fall'])
   
   seasonal_average = data.groupby('Season', observed=False)['PRCP'].mean()

   sns.set()
   plt.figure(figsize=(12, 8))
   sns.barplot(x=seasonal_average.index, y=seasonal_average, hue=seasonal_average.index, palette='pastel', legend=False)
   plt.title("Average Rainfall Across Seasons in Seattle (2014)") 
   plt.xlabel("Season")
   plt.ylabel("Average Rainfall (inches)")
   plt.show()

   highest_rainfall_month = seasonal_average.idxmax()
   lowest_rainfall_month = seasonal_average.idxmin()

   print(f"\nHighest average rainfall: {highest_rainfall_month} ({seasonal_average.max():.2f} inches)")
   print(f"\nLowest average rainfall: {lowest_rainfall_month} ({seasonal_average.min():.2f} inches)")

def threshold_analysis(data):
   """Categorize rainfall into light, moderate, and heavy rain."""

   light_threshold = 0.1
   moderate_threshold = 0.5
   heavy_threshold = 1.0

   data['Rain Category'] = pd.cut(data['PRCP'],
                                  bins=[-np.inf, light_threshold, moderate_threshold, heavy_threshold, np.inf],
                                  labels=['No Rain', 'Light Rain', 'Moderate Rain', 'Heavy Rain'])
   
   category_counts = data['Rain Category'].value_counts()

   sns.set()
   plt.figure(figsize=(12, 8))
   sns.barplot(x=category_counts.index, y=category_counts, hue=category_counts.index, palette='coolwarm', legend=True)
   plt.title("Distribution of Rain Categories in Seattle (2014)")
   plt.xlabel("Rain Category")
   plt.ylabel("Number of Days")
   plt.show()

   print("\nRain Category Distribution:")
   print(category_counts)

def trend_analysis(data):
   """Explore trends or patterns in rainfall over the course of the year."""
   
   # Calculate monthly average rainfall
   monthly_average = data['PRCP'].resample('ME').mean().dropna()

   # Perform linear regression to identify the trend
   slope, intercept, r_value, p_value, std_err = linregress(range(len(monthly_average)), monthly_average)

   # Generate trend line values
   trend_line = intercept + slope * range(len(monthly_average))

   # Plot the trend analysis
   sns.set(style='whitegrid', palette='pastel')
   plt.figure(figsize=(12, 8))
   sns.scatterplot(x=monthly_average.index, y=monthly_average, color='skyblue', label='Monthly Average')
   plt.plot(monthly_average.index, trend_line, color='orange', linestyle='dashed', linewidth=2, label='Trend Line')
   plt.title("Monthly Average Rainfall and Trend in Seattle (2014)", fontsize=16)
   plt.xlabel("Month", fontsize=14)
   plt.ylabel("Average Rainfall (inches)", fontsize=14)
   plt.legend()
   plt.show()

def extreme_events_analysis(data):
   """Identify and analyze extreme rainfall events or outliers."""

   # Calculate the Z-score for rainfall
   z_scores = zscore(data['PRCP'])

   # Define a threshold for extreme events
   threshold = 2.5

   # Identify extreme events based on the threshold
   extreme_events = data.loc[np.abs(z_scores) > threshold]

   # Plot extreme events on a calendar or timeline
   sns.set(style='whitegrid', palette='pastel')
   plt.figure(figsize=(12, 8))
   sns.scatterplot(x=extreme_events.index, y=extreme_events['PRCP'], color='red', label='Extreme Events')
   plt.title("Extreme Rainfall Events in Seattle (2014)", fontsize=16)
   plt.xlabel("Date", fontsize=14)
   plt.ylabel("Rainfall (inches)", fontsize=14)
   plt.legend()
   plt.show()

def correlation_analysis(data):
   """Explore correlations between rainfall and other meteorological factors."""

   # Select relevant columns for correlation analysis
   columns_of_interest = ['PRCP', 'TMAX', 'TMIN', 'AWND', 'WSF2', 'WSF5', 'WT01', 'WT02', 'WT03']
   selected_data = data[columns_of_interest]

   # Calculate the correlation matrix
   correlation_matrix = selected_data.corr()

   # Plot the correlation matrix heatmap
   sns.set(style='whitegrid', font_scale=1.2)
   plt.figure(figsize=(12, 8))
   sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=.5)
   plt.title("Correlation Matrix: Rainfall and Meteorological Factors", fontsize=16)
   plt.show()

def interactive_rainfall_plot(data):
   """Create an interactive rainfall visualization using Plotly."""
   
   data.reset_index(inplace=True)
   # Suppress FutureWarnings
   warnings.simplefilter(action='ignore', category=FutureWarning)
   
   # Create an interactive line plot using Plotly Express
   fig = px.line(data, x='DATE', y='PRCP', title='Rainfall Over Time',
               labels={'PRCP': 'Rainfall (inches)', 'DATE': 'Date'},
               template='plotly_dark')

   # Add interactive features like zooming and panning
   fig.update_xaxes(rangeslider_visible=True)

   # Show the plot 
   fig.show()

def machine_learning_prediction(data):
   """Explore machine learning models for predicting future rainfall based on historical data."""

   # Feature selection (adjust columns based on dataset)
   features = data[['TMAX', 'TMIN', 'AWND', 'WDF2', 'WDF5', 'WSF2', 'WSF5']]

   # Target variable
   target = data['PRCP']
   
   # Split the data into training and testing sets
   X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

   # Choose a model (Random Forest Regressor)
   model = RandomForestRegressor(n_estimators=100, random_state=42)
   model.fit(X_train, y_train)

   # Make predictions
   y_pred = model.predict(X_test)

   # Evaluate the model
   mse = mean_squared_error(y_test, y_pred)
   print(f"Mean Squared Error: {mse:.2f}")

   # Visualize the predictions
   plt.scatter(X_test.index, y_test, label='Actual Rainfall', color='blue')
   plt.scatter(X_test.index, y_pred, label='Predicted Rainfall', color='red')
   plt.title("Actual vs. Predicted Rainfall")
   plt.xlabel("Date")
   plt.ylabel("Rainfall (inches)")
   plt.legend()
   plt.show()

def choose_plot():
   """Allow the user to choose which plot to display."""

   while True:
      print("Choose a plot to display:")
      print("1. Rainfall Histogram")
      print("2. Monthly Average Rainfall")
      print("3. Seasonal Analysis")
      print("4. Threshold Analysis")
      print("5. Trend Analysis")
      print("6. Extreme Events Analysis")
      print("7. Correlation Analysis")
      print("8. Interactive Rainfall Plot")
      print("9. Machine Learning Prediction")
      print("0. Exit")
      
      choice = int(input("Enter the number of the plot you want to see (1-9): "))

      if choice == 0:
         print("Exiting the program.")
         break
      elif choice == 1:
         plot_rainfall_histogram(rainfall)
      elif choice == 2:
         plot_monthly_average(data)
      elif choice == 3:
         plot_seasonal_analysis(data)
      elif choice == 4:
         threshold_analysis(data)
      elif choice == 5:
         trend_analysis(data)
      elif choice == 6:
         extreme_events_analysis(data)
      elif choice == 7:
         correlation_analysis(data)
      elif choice == 8:
         interactive_rainfall_plot(data)
      elif choice == 9:
         machine_learning_prediction(data)
      else:
         print("Invalid choice. Please enter a number between 1 and 9.")

if __name__ == '__main__':
   file_path = "Seattle2014.csv"
   data = load_data(file_path)

   rainfall = data["PRCP"].values.astype(float) / 254.0

   choose_plot()