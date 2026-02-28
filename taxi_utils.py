
'''
File: taxi_utils.py
--------------------------------------
Project Phase 1

Team D:
- Ronnie Chan (27206003)
- Patrice Gallant (40301020)
- Nesrine Larbi (40079009)
--------------------------------------
This file contains 2 classes: TaxiData and TaxiDDA
'''

# Import required libraries
import numpy as np
import pandas as pd
import scipy
import matplotlib.pyplot as plt
import seaborn as sns
import os
import openmeteo_requests
import requests_cache
from retry_requests import retry

# ---------------
# Class TaxiDDA
# ---------------
# This class manages data retrieval
class TaxiData:
   def __init__(self):
      """Constructor"""
      self.base_url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/'
      self.base_file = 'yellow_tripdata_2025-'
      self.months = ["06", "07"]
    

   def download_data(self): 
      """Download the taxi trips data for June and July 2025 using URL."""

      for mm in self.months:
         file = f"{self.base_file}{mm}.parquet"
         if not os.path.exists(file):
            print(f"Downloading {file}...")
            os.system(f"curl -L -O {self.base_url}{file}")

      print(">> All files are saved to local disk.")


   def download_taxi_zones(self):
      """Download the taxi zones lookup table using URL."""
   
      file_name = 'taxi_zone_lookup.csv'
      if not os.path.exists(file_name):
         url = f"https://d37ci6vzurychx.cloudfront.net/misc/{file_name}"
         os.system(f"curl -L -O {url}")

      print(">> Taxi Lookup Table successfully downloaded")


   def download_weather_api(self):
      """
      Download NY Weather using API
      
      The code is taken from Open-Weather API documentation with specified parameters (see params)
      """
      # Setup the Open-Meteo API client with cache and retry on error
      cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
      retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
      openmeteo = openmeteo_requests.Client(session = retry_session)

      # Make sure all required weather variables are listed here
      # The order of variables in hourly or daily is important to assign them correctly below
      url = "https://archive-api.open-meteo.com/v1/archive"
      params = {
         "latitude": 40.7143,
         "longitude": -74.006,
         "start_date": "2025-06-01",
         "end_date": "2025-07-31",
         "hourly": ["temperature_2m", "precipitation"],
         "timezone": "America/New_York",
      }
      responses = openmeteo.weather_api(url, params=params)


      # Process first location. Add a for-loop for multiple locations or weather models
      response = responses[0]
      print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
      print(f"Elevation: {response.Elevation()} m asl")
      print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
      print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

      # Process hourly data. The order of variables needs to be the same as requested.
      hourly = response.Hourly()
      hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy().astype('float32')
      hourly_precipitation = hourly.Variables(1).ValuesAsNumpy().astype('float32')

      hourly_data = {"date": pd.date_range(
         start = pd.to_datetime(hourly.Time() + response.UtcOffsetSeconds(), unit = "s", utc = True),
         end =  pd.to_datetime(hourly.TimeEnd() + response.UtcOffsetSeconds(), unit = "s", utc = True),
         freq = pd.Timedelta(seconds = hourly.Interval()),
         inclusive = "left"
      )}

      hourly_data["temperature_2m"] = hourly_temperature_2m
      hourly_data["precipitation"] = hourly_precipitation

      hourly_dataframe = pd.DataFrame(data = hourly_data)
      print("\nHourly data\n", hourly_dataframe)
      return hourly_dataframe



# ---------------
# Class TaxiDDA
# ---------------
# This class manages Data Descriptive Analysis (DDA). The methods are from Lab Assignment 2.
class TaxiDDA:
   
   def quantDDA(self, df):
      """
      Generate a summary of advanced statistical information for given pandas DataFrame.
      The resulting summary is a structured pandas DataFrame.

      Parameters
      ----------
      df : pandas.DataFrame
         Input DataFrame

      Returns
      -------
      pandas.DataFrame
         A well-structured summary of advanced statistical information for given DataFrame.
      """

      # Set variables
      column_list = ["feature", "num_observations", "num_entries", "num_unique", "num_missing", "num_outlier",
                  "num_extreme", "mode", "mean", "std", "min", "Q1", "median", "Q3", "max", "skew", "kurtosis"]
      data_list = []

      # Compute the statistics for each column
      for col in df.columns:
         # Common statistical details for both Numerical and Categorical variables
         observ = len(df[col])
         entries = df[col].count()
         unique = len(df[col].unique())
         missing = observ - entries
         mode_values = df[col].mode().values
         if len(mode_values) > 3:
            mode = np.nan
         else:
            mode = str(mode_values[0])

         # Statistics for Numerical Variables
         if pd.api.types.is_numeric_dtype(df[col]):
            mean = np.round(df[col].mean(), 2)      # mean
            std = np.round(df[col].std(), 2)        # standard deviation
            max = df[col].max()                     # maximum
            min = df[col].min()                     # mininum
            Q1 = df[col].quantile(0.25)                           # quartile Q1
            median = np.round(df[col].quantile(0.5), 2)           # quartile Q2 or median
            Q3 = df[col].quantile(0.75)                           # quartile Q3
            IQR = Q3 - Q1                                         # IQR
            lower_outlier = df[col] < (Q1 - 1.5 * IQR)            # Lower outlier
            higher_outlier = df[col] > (Q3 + 1.5 * IQR)           # Upper outlier
            outlier = lower_outlier.sum() + higher_outlier.sum()  # Number of outliers
            lower_extreme = df[col] < df[col].quantile(0.01)      # Bottom 1% extreme value
            higher_extreme = df[col] > df[col].quantile(0.99)     # Top 1% extreme value
            extreme = lower_extreme.sum() + higher_extreme.sum()  # Number of extreme values

            # Compute Skewness and Kurtosis
            # nan_policy = 'omit' ignores Nan values during calculation
            # bias=False treats the data as a Sample (N-1) rather than a Population, matching Pandas behaviour
            skew = np.round(scipy.stats.skew(df[col], nan_policy='omit', bias=False), 3)         # Round Skewness to 3 decimal places for precision
            kurt = np.round(scipy.stats.kurtosis(df[col], nan_policy='omit', bias=False), 3)     # Round Kurtosis to 3 decimal places for precision

            # Reformat the quartiles Q1 and Q3
            Q1 = np.round(Q1, 2)
            Q3 = np.round(Q3, 2)


         # Statistics for Nomical Categorical Variables
         else:
            mean = std = max = min = Q1 = median = Q3 = outlier = extreme = skew = kurt = np.nan

         # Append the statistics of the column to the resulting list
         data_list.append([col, observ, entries, unique, missing, outlier, extreme, mode, mean, std, min, Q1, median, Q3, max, skew, kurt])

      # Convert to Numpy array
      np_data = np.array(data_list)

      # Convert to pandas DataFrame and return the summary
      return pd.DataFrame(np_data, columns = column_list)
   
   
   
   def vizDDA(self, df):
      """
      Generates a square grid of plots for a given pandas Dataframe.

      Parameters
      ----------
      df : pandas.DataFrame
         Input DataFrame to perform Data Visualization

      Returns
      -------
      None

      """

      # 1. Create a copy of the DataFrame (for plotting the square grid)
      viz_df = df.copy()

      # 2. Drop non-relevant columns from the copy DataFrame
      # The non-relevant columns are object types with too many unique values
      nonrelevant = []
      for feat in viz_df.columns:
         if not self.is_categorical(viz_df, feat) and viz_df[feat].dtype == 'object':
            nonrelevant.append(feat)
      viz_df.drop(nonrelevant, axis=1, inplace=True)

      # 3. Set the variables with the updated DataFrame
      features = viz_df.columns
      length = len(features)

      # 4. Populate the subplots
      fig, ax = plt.subplots(nrows=length, ncols=length, figsize=(23,23))
      for row in range(length):
         y_feature = features[row]

         for col in range(length):
            x_feature = features[col]

            # 5. Plot Univariate charts on the main diagonal
            if x_feature == y_feature:

               # -- Categorical Univariate: Bar plot
               if self.is_categorical(viz_df, x_feature):
                  sns.countplot(data=viz_df, x=x_feature, color='black', ax=ax[row, col])

               # -- Continuous Univariate: Histogram
               else:
                  ax[row, col].hist(data=viz_df, x=x_feature, color='black')


            # 6. Plot Bivariate charts on the off-diagonal area
            else:

               # -- Datetime: Line plot
               if pd.api.types.is_datetime64_any_dtype(viz_df[x_feature]):
                  sns.lineplot(data=viz_df, x=x_feature, y=y_feature, color='MediumAquamarine', ax=ax[row, col])

               # -- Categorical vs Categorical: Bar plot
               if self.is_categorical(viz_df, x_feature) and self.is_categorical(viz_df, y_feature):
                  sns.countplot(data=viz_df, x=x_feature, hue=y_feature, palette='Set2', ax=ax[row, col])

               # -- Categorical vs Continous: Vertical Box plot
               elif self.is_categorical(viz_df, x_feature) and not self.is_categorical(viz_df, y_feature):
                  sns.boxplot(data=viz_df, x=x_feature, y=y_feature, color='MediumAquamarine', ax=ax[row, col])

               # -- Continous vs Categorical: Horizontal Box plot
               elif not self.is_categorical(viz_df, x_feature) and self.is_categorical(viz_df, y_feature):
                  sns.boxplot(data=viz_df, x=x_feature, y=y_feature, color='MediumAquamarine', ax=ax[row, col], orient='h')

               # -- Continous vs Continous: Scatterplot
               else:
                  sns.scatterplot(data=viz_df, x=x_feature, y=y_feature, color='MediumAquamarine', ax=ax[row, col])

            # 7. Label x and y axes
            ax[row, col] = self.label_axis(ax[row, col], row, col, length, x_feature, y_feature)

      # 8. Display Grid of plots
      plt.show();

      # 9. Display Heatmap for missing values -- using given original DataFrame
      plt.figure(figsize=(6,6))
      sns.heatmap(df.isnull(),
                  cmap =['black', 'MediumAquamarine'],
                  cbar=True,
                  cbar_kws={'label': 'Missing Values'});
      plt.title("Missing Values Heatmap")
      plt.xlabel("Columns")
      plt.ylabel("RowID")
      plt.show();
   
   # -------------------------------
   # Helper function: is_categorical
   # -------------------------------
   def is_categorical(self, df, feature):
      """
      Check if the given feature is categorical.

      Parameters
      ----------
      df : pandas.DataFrame
         Input DataFrame
      feature : str
         Name of the feature to check

      Returns
      -------
      bool
         True if the feature is categorical, False otherwise
      """

      # Nominal Variable
      if (df[feature].dtype == "object") and (df[feature].nunique() <= 10):
         return True

      # Ordinal Variable
      if (df[feature].dtype == 'int64') and (df[feature].nunique() <= 10):
         return True

      return False

   # ---------------------------
   # Helper function: label_axis
   # ---------------------------
   def label_axis(self, ax_obj, row, col, length, x_feature, y_feature):
      """
      Customizes axis labels for a subplot at the location [row, col] of the grid.

      Parameters
      ----------
      ax_obj : matplotlib.axes.Axes
         Axes object
      row : int
         Row index of the subplot
      col : int
         Column index of the subplot
      length : int
         Size of the square grid
      x_feature : Str
         Name of the x-axis feature
      y_feature : Str
         Name of the y-axis feature

      Returns
      -------
      ax_obj : matplotlib.axes.Axes
         Labelled axes object
      """
      ax_obj.set(xlabel = '', ylabel = '')     # Remove labels for inner subplots (by default)

      # Label x-axis of the top grid
      if row == 0:
         sec_ax = ax_obj.secondary_xaxis('top')  # Enable top x axis
         sec_ax.set_xlabel(x_feature)            # Label the top x axis
         sec_ax.set_xticks([])                   # Remove ticks on x axis
         sec_ax.spines['top'].set_visible(False) # Remove spices on x axis

         if col == 0:
            ax_obj.set(ylabel=y_feature)

      # Label x-axis and y-axis of the bottom-left subplot
      elif (row == length - 1 and col == 0):
         ax_obj.set(xlabel=x_feature, ylabel=y_feature)

      # Label x-axis of the bottom grid
      elif (row == length - 1):
         ax_obj.set(xlabel=x_feature)

      # Label y-axis of the leftmost column
      elif col == 0:
         ax_obj.set(ylabel=y_feature)

      return ax_obj

      

    
