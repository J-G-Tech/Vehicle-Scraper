
import os

from  Lister  import  Lister
import json

my_account_id = 'account1'



def publish_single_product(product_file):
    lister = Lister()
    if lister.login(my_account_id):
        import glob
        import re

        # Extract the directory path from the product_file
        directory_path = os.path.dirname(product_file)
        # Append /images to the directory path
        images_directory = os.path.join(directory_path, 'images')

        # Get list of all image files in the images directory
        image_files = glob.glob(images_directory + '/*')

        # Iterate over each image file
        for image_file in image_files:
            # Extract the number from the image file name using regex
            number = re.findall(r'\d+', os.path.basename(image_file))
            # If the number is greater than 20, delete the image file
            if number and int(number[0]) > 20:
                os.remove(image_file)

        with open(product_file, 'r') as f:
            product_data = json.load(f)
        formatted_product = format_product(product_data)
        lister.list(formatted_product)

def format_product(product):
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
        'automatic': 'Automatic transmission',
        'manual': 'Manual transmission'
    }

    fuel_type_mapping = {
        'diesel': 'Diesel',
        'Diesel': 'Diesel',
        'electric': 'Electric',
        'gasoline': 'Gasoline',
        'flex': 'Flex',
        'hybrid': 'Hybrid',
        'petrol': 'Petrol',
        'plug in hybrid': 'Plug in hybrid'
    }

   
    # Extracting information
    information = product['information']
     # Extracting MPG information
    mpg_info = information.get('City/Highway', '0/0 MPG')
    city_mpg, highway_mpg = map(int, mpg_info.split(' ')[0].split('/'))
    body_style = information.get('Body Style', '').lower()
    exterior_color = information.get('Exterior Color', '').lower()
    interior_color = information.get('Interior Color', '').lower()
    transmission = information.get('Transmission', '').lower()
    fuel_type = information.get('Engine', '').lower()
    # Mapping information
    body_style = body_style_mapping.get(body_style, 'Other')
    exterior_color = next((v for k, v in color_mapping.items() if k in exterior_color), 'Black')
    interior_color = next((v for k, v in color_mapping.items() if k in interior_color), 'Black')
    transmission = next((v for k, v in transmission_mapping.items() if k in transmission), 'Automatic transmission')
    fuel_type = next((v for k, v in fuel_type_mapping.items() if k in fuel_type), 'Other')
    mileage = information.get('Mileage', 300)
    image_folder = os.path.join('vehicle_listings', 'unposted', f'{product["name"]}_{product["information"]["VIN"]}', 'images')
    images = [{'file': os.path.abspath(os.path.join(image_folder, f))} for f in os.listdir(image_folder) if f.endswith('.jpg')]
    images = images[:20] 
    price = int(''.join(filter(str.isdigit, product['price']))) if '$' in product['price'] else 5000
    name_parts = product["name"].split("__")
    year = name_parts[0]
    make = name_parts[1].split("_")[0]
    condition = "Excellent"
    features = product.get('features', [])
    features_string = "\n".join([f"⚡️{feature}" for feature in features])
    print(features_string)
    if mileage == 300:
        description = f"CALL OR TEXT (4️⃣3️⃣4️⃣) 8️⃣5️⃣7️⃣ - 6️⃣6️⃣4️⃣3️⃣\n\nBRAND NEW VEHICLE\n\n{features_string}\n\n🥂 MPG CITY: {city_mpg}\n🥂 MPG HIGHWAY: {highway_mpg}\n\nEXTERIOR COLOR: {exterior_color}\nINTERIOR COLOR: {interior_color}\n\nCOMES WITH FULL MANUFACTURE WARRANTY\n\ndisclaimer: sale price does not include sales tax (4.35%), state titling fees, or $689 processing fee. (VADLR)\n\npayments applicable assuming credit approval"
    else:
        description = f"CALL OR TEXT (4️⃣3️⃣4️⃣) 8️⃣5️⃣7️⃣ - 6️⃣6️⃣4️⃣3️⃣\n\n{mileage} MILES ON ODOMETER\n\n{features_string}\n\n🥂 MPG CITY: {city_mpg}\n🥂 MPG HIGHWAY: {highway_mpg}\n\nEXTERIOR COLOR: {exterior_color}\nINTERIOR COLOR: {interior_color}\n\nvehicle will undergo a 72-point inspection and a full detail! We put the money into any possible repairs up front so you don't have to!\n\n💎 COMES WITH A 30 DAY/1,000 MILE LIMITED POWERTRAIN WARRANTY (additional warranty can be purchased)\n\ndisclaimer: sale price does not include sales tax (4.35%), state titling fees, or $689 processing fee. (VADLR)\n\npayments applicable assuming credit approval"
    

    model = "_".join(name_parts[1].split("_")[1:])
    link_parts = product["link"].split("-")
    if len(link_parts) > 3:
        model += " " + link_parts[-2]
    model = model.replace("_", " ")
    print(len(images))
    return {
        'title': product['name'],
        'year': year,
        'make': make,
        'model': model,
        'price': price,
        'images': images[:20],
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
        'transmission': transmission,
        'description' : description
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


