import pandas as pd
import json
import random
import matplotlib.pyplot as plt 
import matplotlib

from django.core.serializers import serialize

from vendors.models import ProductCategory,Product

def data_process(df):
    print(df)
    grouped_df = df.groupby('Category').agg({
    'Items Sold': 'sum'}).reset_index()

    # Print the grouped DataFrame
    print(grouped_df)
    
    # Generate background colors dynamically using a color map
    cmap = plt.get_cmap('Accent')  # You can choose a different colormap
    colors = [matplotlib.colors.rgb2hex(cmap(i)[:3]) for i in range(len(grouped_df['Category']))]
    print(colors)

    

    # Convert DataFrame to JSON
    chart_data = {
        'labels': grouped_df['Category'].tolist(),
        'datasets': [{
            'data': grouped_df['Items Sold'].tolist(),
            'backgroundColor': colors,
        }],
    }

    
    print(chart_data)
    # # Convert ProductCategory instances to JSON-serializable format
    # categories = Product.objects.values('item_name')
    # chart_data['labels'] = [category['item_name'] for category in categories]
    #     # Convert to JSON string
    chart_data_json = json.dumps(chart_data)

    print(chart_data_json)
    return chart_data_json