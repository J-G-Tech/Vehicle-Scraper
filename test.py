import os
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import re 


class Vehicle:
    def __init__(self, features, information, price, name,  link):
        self.features = features
        self.information = information
        self.price = price
        self.name = name
        self.link = link


def scrape_links(page_url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(page_url)

    elements = driver.find_elements(By.CLASS_NAME, 'hero-carousel__item--viewvehicle')
    print(f"Found {len(elements)} elements.")
    links = set()

    for element in elements:
        link = element.get_attribute('href')
        if link:
            links.add(link)
            print(f"Found link: {link}")
    print(f"Found {len(links)} links.")

    

    if not links:
        print("No links found with the specified class name.")
    

    # Look for the "next" button on the main page
    
    next_page_element = driver.find_element(By.CSS_SELECTOR, 'a.stat-arrow-next')
    next_page_link = next_page_element.get_attribute('href')
    
    
    print("next page link", next_page_link)
    driver.quit()
    return next_page_link, links


def extract_vehicle_features(page_url):
    print("Entering extract_vehicle_features function")
    
    response = requests.get(page_url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    vehicle_highlights_list = soup.find('ul', {'id': 'vehicle-highlights-list'})

    vehicle_features = []
    if vehicle_highlights_list:
        vehicle_highlights_items = vehicle_highlights_list.find_all('li')
        for item in vehicle_highlights_items:
            feature_label = item.find('span')
            if feature_label:
                vehicle_features.append(feature_label.text.strip())

    print("Exiting extract_vehicle_features function")
    return vehicle_features



def download_images(page_url, vehicle_name, vehicle_vin):
    print("Entering download_images function")
    base_url = 'https://www.pinkertonlynchburg.com'
    
    response = requests.get(page_url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    image_tags = soup.find_all('a', {'href': re.compile('/inventoryphotos')})

    # Create directories if they don't exist
    if not os.path.exists('vehicle_listings'):
        os.makedirs('vehicle_listings')
    folder_name = f'{vehicle_name}_{vehicle_vin}'
    if not os.path.exists(f'vehicle_listings/{folder_name}'):
        os.makedirs(f'vehicle_listings/{folder_name}')
    if not os.path.exists(f'vehicle_listings/{folder_name}/images'):
        os.makedirs(f'vehicle_listings/{folder_name}/images')
    for img in image_tags:
        img_url = img['href']
        print(f"Checking URL: {img_url}")
        if vehicle_vin.lower() in img_url:
            print(f"Matched VIN in URL: {img_url}")
            if img_url.startswith('/'):
                img_url = base_url + img_url
            response = requests.get(img_url, stream=True)
            if response.status_code == 200:
                print(f"Downloading image from: {img_url}")
                with open(f'vehicle_listings/{folder_name}/images/{img_url.split("/")[-1]}', 'wb') as out_file:
                    out_file.write(response.content)
            else:
                print(f"Failed to download image. Status code: {response.status_code}")

    print("Exiting download_images function")


def extract_vehicle_price(page_url):
    print("Entering extract_vehicle_price function")
    
    response = requests.get(page_url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    vehicle_price_div = soup.find('div', {'class': 'vehiclePricingHighlight featuredPrice'})

    vehicle_price = None
    if vehicle_price_div:
        vehicle_price_span = vehicle_price_div.find('span', {'class': 'vehiclePricingHighlightAmount'})
        if vehicle_price_span:
            vehicle_price = vehicle_price_span.text.strip()

    print("Exiting extract_vehicle_price function")
    return vehicle_price

def extract_vehicle_name(page_url):
    print("Entering extract_vehicle_name function")
   
    response = requests.get(page_url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    vehicle_name_h2 = soup.find('h2', {'class': 'vehicle-title__text'})

    vehicle_name = None
    if vehicle_name_h2:
        vehicle_name_span = vehicle_name_h2.find('span', {'class': 'vehicle-title__year-make-model'})
        if vehicle_name_span:
            vehicle_name = vehicle_name_span.text.strip()

    print("Exiting extract_vehicle_name function")
    vehicle_name = vehicle_name.replace(" ", "_").replace("\n", "")
    return vehicle_name


def extract_vehicle_info(page_url):
    print("Entering extract_vehicle_info function")
    
    response = requests.get(page_url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    info_items = soup.find_all('li', class_='info__item')

    vehicle_info = {}

    for item in info_items:
        label = item.find('span', class_='info__label').text.strip()
        value = item.find('span', class_='info__value')
        if value:
            vehicle_info[label] = value.get('title', '').strip()

    # Extract VIN
    vin_span = soup.find('span', class_='vehicle-identifiers__value')
    if vin_span:
        vehicle_info['VIN'] = vin_span.text.strip()

    print("Exiting extract_vehicle_info function")
    return vehicle_info


def main():
    driver_path = 'chromedriver.exe'
    page_url = "https://www.pinkertonlynchburg.com/new-trucks.html?pt=1"


    
    while page_url:
        page_url,page_links = scrape_links(page_url)
        print(len(page_links))
        for link in page_links:
            features = extract_vehicle_features(link)
            price = extract_vehicle_price(link)
            name = extract_vehicle_name(link)
            vehicle_info = extract_vehicle_info(link)

            # Create a Vehicle object
            vehicle = Vehicle(features, vehicle_info, price, name,  link)

            # Download images
            download_images(link, name, vehicle_info['VIN'])

            # Write the vehicle attributes to a JSON file
            with open(f'vehicle_listings/{name}_{vehicle_info["VIN"]}/attributes.json', 'w') as json_file:
                json.dump(vehicle.__dict__, json_file)


if __name__ == "__main__":

    main()



#TO-DO:
#Scrape: MPG, Car title, vehicle information, price, and the pictures
#then we need to categorize these features into the facebook features
