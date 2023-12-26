import pandas as pd
import simplejson as json
import random
import calendar
import matplotlib.pyplot as plt 
import matplotlib

from django.core.serializers import serialize

from vendors.models import ProductCategory,Product

def data_process(df):
    print(df)
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

    
    print(monthly_items_sold)
    print(type(monthly_items_sold))
    df3 = pd.DataFrame(monthly_items_sold)
    df3.reset_index(inplace = True)
    df3['Month'] = df3['Month'].apply(lambda x: calendar.month_abbr[x])


    # Convert DataFrame to JSON
    line_chart_data = {
        'labels': df3['Month'].tolist(),
        'datasets': [{
            "label":"Total Sales",
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
   

   
    return chart_data_json,line_chart_data_json,line_chart_data_price_json

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
    print(line_chart_data_price_json)


    return line_chart_data_price_json