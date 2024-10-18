import os
import pandas as pd

from django.shortcuts import render
from django.http import HttpResponse, FileResponse

# Create your views here.
def home(request):
    return render(request, 'getcsvfile/home.html')

def submit_form(request):
    input_file = request.FILES['input-csv']
    df = pd.read_csv(input_file)

    diamond_shape_list = df['data__diamond_can_be_matched_with'][0].split(",")
    diamond_metal_name_obj = df['data__metal_name']
    diamond_product_name_obj = df['data__product_name']
    diamond_sku_obj = df['Product sku']
    diamond_description_obj = df['data__product_description']
    diamond_quatity_obj = df['data__qty']

    COUNT = 0
    diamond_data_list = []
    for diamond_shape in diamond_shape_list:
        for key, _  in diamond_metal_name_obj.items():
            COUNT += 1
            diamond_row_obj = {
                'ID': COUNT,
                'Variation': 'variation',
                'SKU': diamond_sku_obj[key] + "-" + diamond_shape,
                'Name': diamond_product_name_obj[key] + " with " + diamond_shape,
                'Published': 1,
                'Is featured?': 0,
                'Visibility in catalog': 'visible',
                'Short description': "",
                'Description': diamond_description_obj[key],
                'Stock': diamond_quatity_obj[key],
                'Price': 100,
            }
            diamond_data_list.append(diamond_row_obj)

    diamond_df = pd.DataFrame(diamond_data_list)
    output_path = 'E://expected_output.csv' if os.path.exists('E://') else 'D://expected_output.csv'
    diamond_df.to_csv(output_path, index=False)
    return render(request, 'getcsvfile/download.html')

def download_csv(request):
    file_path = 'E://expected_output.csv' if os.path.exists('E://') else 'D://expected_output.csv'
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename='expected_output.csv')
        return response
    else:
        return HttpResponse("File not found.")