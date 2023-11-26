
import os

"""
test_product = {
    'title': String, # Required
    'price': String, # Required
    'images' : [
        {"file": "xxx.jpg"}و
        {"file": "xxx.jpg"}و
        ...
        ...
    ]و # Required
    'location': String, # Optional : Required by facebook. If left empty the default value will be used. Default value can be changed at elements.json file.
    'category': String,  # Optional : Required by facebook. If left empty the default value will be used. Default value can be changed at elements.json file.
    'condition': String,  # Optional : Required by facebook. If left empty the default value will be used. Default value can be changed at elements.json file.
    'hide_from_friends' : Boolean, # Optional : Optional for facebook. Default value is False.
    'sku': String, # Optional : Optional for facebook. Default value is None.
}
"""

from  Lister  import  Lister
import json

my_account_id = 'account1'

product = {
	'title': '...', 
	'price': '...', 
	'images': [
		{'file' : '/image.jpg'},
	],
}

def publish_single_product(product_file):
    lister = Lister()
    if lister.login(my_account_id):
        with open(product_file, 'r') as f:
            product_data = json.load(f)
        formatted_product = format_product(product_data)
        lister.list(formatted_product)
        
#def publish_multi_products():
  #  my_json_file = open('products.json', 'r')
  #  products = json.load(my_json_file)['products']

   # lister = Lister()
  #  if  lister.login(my_account_id) :
 #       for product in products : 
   #         result = lister.list(product)
   #         if result: print('Success!')

def format_product(product):
    # Mapping dictionaries
    body_style_mapping = {
        'coupe': 'Coupe',
        'truck': 'Truck',
        'sedan': 'Sedan',
        'hatchback': 'Hatchback',
        'suv': 'SUV',
        'convertible': 'Convertible',
        'wagon': 'Wagon',
        'minivan': 'Minivan',
        'small car': 'Small car',
        'crew cab': 'Truck'
    }

    color_mapping = {
        'black': 'Black',
        'blue': 'Blue',
        'brown': 'Brown',
        'gold': 'Gold',
        'green': 'Green',
        'gray': 'Gray',
        'pink': 'Pink',
        'purple': 'Purple',
        'red': 'Red',
        'silver': 'Silver',
        'orange': 'Orange',
        'white': 'White',
        'yellow': 'Yellow',
        'charcoal': 'Charcoal',
        'off white': 'Off white',
        'tan': 'Tan',
        'beige': 'Beige',
        'burgundy': 'Burgundy',
        'turquoise': 'Turquoise'
    }

    transmission_mapping = {
        'automatic': 'Automatic',
        'manual': 'Manual transmission'
    }

    fuel_type_mapping = {
        'diesel': 'Diesel',
        'electric': 'Electric',
        'gasoline': 'Gasoline',
        'flex': 'Flex',
        'hybrid': 'Hybrid',
        'petrol': 'Petrol',
        'plug in hybrid': 'Plug in hybrid'
    }

    # Extracting information
    information = product['information']
    body_style = information.get('Body Style', '').lower()
    exterior_color = information.get('Exterior Color', '').lower()
    interior_color = information.get('Interior Color', '').lower()
    transmission = information.get('Transmission', '').lower()
    fuel_type = information.get('Engine', '').lower()

    # Mapping information
    body_style = body_style_mapping.get(body_style, 'Other')
    exterior_color = next((v for k, v in color_mapping.items() if k in exterior_color), 'Other')
    interior_color = next((v for k, v in color_mapping.items() if k in interior_color), 'Other')
    transmission = next((v for k, v in transmission_mapping.items() if k in transmission), 'Manual transmission')
    fuel_type = next((v for k, v in fuel_type_mapping.items() if k in fuel_type), 'Other')
    mileage = information.get('Mileage', 0)
    # Rest of the function...
    image_folder = os.path.join('vehicle_listings', f'{product["name"]}_{product["information"]["VIN"]}', 'images')
    images = [{'file': os.path.abspath(os.path.join(image_folder, f))} for f in os.listdir(image_folder) if f.endswith('.jpg')]
    name_parts = product["name"].split("__")
    year = name_parts[0]
    make = name_parts[1].split("_")[0]
    condition = "Excellent"


    model = "_".join(name_parts[1].split("_")[1:])
    link_parts = product["link"].split("-")
    if len(link_parts) > 3:
        model += " " + link_parts[-2]
    print(images)
    return {
        'title': product['name'],
        'year': year,
        'make': make,
        'model': model,
        'price': product['price'],
        'images': images,
        'location': 'Lynchburg, Virginia',  # Replace with your location
        'category': 'Vehicles',  # Replace with the appropriate category
        'condition': condition,  # Replace with the appropriate condition
        'vehicle type': 'Car/Truck',
        'hide_from_friends': False,
        'mileage': mileage,  # As per your requirement
        'body style': body_style,
        'exterior color': exterior_color,
        'interior color': interior_color,
        'fuel type': fuel_type,
        'transmission': transmission
    }


def publish_multi_products():
    lister = Lister()
    if lister.login(my_account_id) :
        for filename in os.listdir('vehicle_listings'):
            if filename.endswith('.json'):
                with open(os.path.join('vehicle_listings', filename), 'r') as f:
                    product = json.load(f)
                    product = format_product(product)
                    result = lister.list(product)
                    if result: print('Success!')

publish_single_product('vehicle_listings/2023__GMC_Sierra_1500_1GTUUEEL1PZ186658/attributes.json')