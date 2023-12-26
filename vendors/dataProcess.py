import pandas as pd
import simplejson as json
import random
import calendar
import matplotlib.pyplot as plt 
import matplotlib
import numpy as np
from sklearn.linear_model import LinearRegression
import math



from django.core.serializers import serialize

from vendors.models import ProductCategory,Product

def data_process(df):
    # print(df.head())
    chart_data_product_json,forecasts = item_sold_by_product(df)
    # Get unique products
    unique_products = df['Product'].unique()
    

    grouped_df = df.groupby('Category').agg({
    'Items Sold': 'sum'}).reset_index()

    # Generate background colors dynamically using a color map
    cmap = plt.get_cmap('Accent')  # You can choose a different colormap
    colors = [matplotlib.colors.rgb2hex(cmap(i)[:3]) for i in range(len(grouped_df['Category']))]
    
    # Convert DataFrame to JSON
    chart_data = {
        'labels': grouped_df['Category'].tolist(),
        'datasets': [{
            'data': grouped_df['Items Sold'].tolist(),
            'backgroundColor': colors,
        }],
    }

    chart_data_json = json.dumps(chart_data)


    #Items sold per month
    

    df2 = df
    df2['Date'] = pd.to_datetime(df2['Date'])
    #Create a new column for month
    df2['Month'] = df2['Date'].dt.month
    
    
   


    #Group by month and sum the 'Items Sold' column
    monthly_items_sold = df2.groupby('Month')['Items Sold'].sum()

    
   
    df3 = pd.DataFrame(monthly_items_sold)
    df3.reset_index(inplace = True)
    df3['Month'] = df3['Month'].apply(lambda x: calendar.month_abbr[x])


    # Convert DataFrame to JSON
    line_chart_data = {
        'labels': df3['Month'].tolist(),
        'datasets': [{
            "label":"Total Items Sold",
            'data': df3['Items Sold'].tolist(),
            'borderColor':'rgba(54, 162, 235, 0.5)',
            "backgroundColor":'rgba(54, 162, 235, 0.5)',
            'fill': False,
            'tension': 0.1
        }],
    }

    # Convert to JSON string
    line_chart_data_json = json.dumps(line_chart_data)

    # print(df3)
    line_chart_data_price_json = generate_data_month_price(df)
    pie_chart_data_price_json = generate_data_category_price(df)
   

   
    return (chart_data_json,
            line_chart_data_json,
            line_chart_data_price_json,
            pie_chart_data_price_json,
            unique_products,
            chart_data_product_json,
            forecasts)

def generate_data_month_price(df):
    df['Date'] = pd.to_datetime(df['Date'])
    #Create a new column for month
    df['Month'] = df['Date'].dt.month

    #Group by month and sum the 'Items Sold' column
    monthly_items_sold = df.groupby('Month')['Price'].sum()

    df3 = pd.DataFrame(monthly_items_sold)
    df3.reset_index(inplace = True)
    df3['Month'] = df3['Month'].apply(lambda x: calendar.month_abbr[x])

    # Convert DataFrame to JSON
    line_chart_data = {
        'labels': df3['Month'].tolist(),
        'datasets': [{
            "label":"Total Sales in $",
            'data': df3['Price'].tolist(),
            'borderColor':'rgba(54, 162, 235, 0.5)',
            "backgroundColor":'rgba(54, 162, 235, 0.5)',
            'fill': False,
            'tension': 0.1
        }],
    }
    
    # Convert to JSON string
    line_chart_data_price_json = json.dumps(line_chart_data)
    # print(line_chart_data_price_json)


    return line_chart_data_price_json

def generate_data_category_price(df):
    grouped_df = df.groupby('Category').agg({
    'Price': 'sum'}).reset_index()

    # Generate background colors dynamically using a color map
    cmap = plt.get_cmap('Accent')  # You can choose a different colormap
    colors = [matplotlib.colors.rgb2hex(cmap(i)[:3]) for i in range(len(grouped_df['Category']))]
    
    # Convert DataFrame to JSON
    chart_data = {
        'labels': grouped_df['Category'].tolist(),
        'datasets': [{
            'data': grouped_df['Price'].tolist(),
            'backgroundColor': colors,
        }],
    }

    chart_data_json = json.dumps(chart_data)
    
    return chart_data_json


def item_sold_by_product(df):
    unique_products = df['Product'].unique()
    # print(unique_products)

    # Convert the 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    #Filter out data of 2023
    df = df[df['Date'].dt.year == 2023]


    # Create new columns for month and year
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year

    # Group by 'Product Category', 'Month', and 'Year' and sum the 'Items Sold'
    result = df.groupby(['Product', 'Month', 'Year'])['Items Sold'].sum().reset_index()
    forecasts = forecast_sales_using_regression(result)
    result['Month'] = result['Month'].apply(lambda x: calendar.month_abbr[x])
    # print("******************")
    # print(result)
    

    # Convert the result to JSON format for Chart.js
    chart_data = result.groupby('Product').apply(lambda x: x[['Month', 'Year', 'Items Sold']].to_dict(orient='records')).to_dict()

    chart_data_product_json = json.dumps(chart_data)

    return chart_data_product_json,forecasts


def forecast_sales_using_regression(df):
    # Assuming your dataframe is named df
    # Convert the 'Month' column to numeric values (assuming 'Jan' is 1, 'Feb' is 2, and so on)
    # month_mapping = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
    # df['Month'] = df['Month'].map(month_mapping)

    # Create a new feature 'Month-Year' as a combination of 'Year' and 'Month'
    df['Month-Year'] = df['Year'].astype(str) + '-' + df['Month'].astype(str)

    # Create a dictionary to store linear regression models and forecasts for each product
    linear_models = {}
    forecasts = {}

    # Iterate over unique products in the dataframe
    for product in df['Product'].unique():
        # Filter data for the current product
        product_data = df[df['Product'] == product][['Month-Year', 'Items Sold']]
        
        # Convert 'Month-Year' to numeric values for regression
        product_data['Month-Year'] = pd.to_numeric(product_data['Month-Year'].str.replace('-', ''), errors='coerce')
        
        # Drop rows with NaN values (if any)
        product_data = product_data.dropna(subset=['Month-Year', 'Items Sold'])
        
        # Extract features (X) and target variable (y)
        X = product_data[['Month-Year']]
        y = product_data['Items Sold']
        
        # Create a linear regression model
        model = LinearRegression()
        
        # Fit the model to the existing data
        model.fit(X, y)
        
        # Predict sales for the next month
        next_month = int(X['Month-Year'].max()) + 1  # Assuming the next month is the next sequential value
        forecast = model.predict([[next_month]])
        
        # Store the model and forecast in dictionaries
        linear_models[product] = model
        forecasts[product] = math.floor(forecast[0])

        # Print the forecast for each product
        # print(f'Forecast for {product} in the next month: {forecast[0]}')
        
    # print(forecasts)
    return forecasts
        
