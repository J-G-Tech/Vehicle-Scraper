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
class Vehicle:
    def __init__(self, features, information, price, name, pictures, html):
        self.features = features
        self.information = information
        self.price = price
        self.name = name
        self.pictures = pictures
        self.html = html

def scrape_links_and_download_html(driver_path, page_url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(page_url)

    # Wait for the elements to be loaded before trying to find them
    

    elements = driver.find_elements(By.CLASS_NAME, 'hero-carousel__item--viewvehicle')
    links = set()

    for element in elements:
        link = element.get_attribute('href')
        if link:
            links.add(link)

    html_contents = []

    if not links:
        print("No links found with the specified class name.")
    else:
        for link in links:
            # Check if the HTML file for this link already exists in the downloaded_html_files directory
            file_name = 'downloaded_html_files/' + link.split('/')[-1] + '.html'
            if os.path.exists(file_name):
                #print(f"HTML file for {link} already exists. Skipping download.")
                continue

            driver.get(link)
            html_content = driver.page_source

            if not html_content:
                print("No HTML content found for the current page.")
            else:
                html_contents.append(html_content)
            # Go back to the main page after scraping each vehicle
            driver.back()

    if not html_contents:
        print("No HTML contents to write to files.")
    else:
        # Create a directory for the downloaded HTML files if it doesn't exist
        if not os.path.exists('downloaded_html_files'):
            os.makedirs('downloaded_html_files')

        for i, content in enumerate(html_contents, start=1):
            with open(f'downloaded_html_files/linked_page_{i}.html', 'w', encoding='utf-8') as file:
                file.write(content)

    # Look for the "next" button on the main page
    next_page_element = driver.find_element(By.CLASS_NAME, 'stat-arrow-next')
    next_page_link = next_page_element.get_attribute('href')
    
    print("next page link", next_page_link)
    driver.quit()
    return html_contents, next_page_link

def extract_vehicle_features(html_file):
    print("Entering extract_vehicle_features function")
    
    html_content = html_file

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

def download_images(html_content, listing_name):
    print("Entering download_images function")
    base_url = 'https://www.pinkertonlynchburg.com'
    
    soup = BeautifulSoup(html_content, 'html.parser')
    image_tags = soup.find_all('img')

    # Create directories if they don't exist
    if not os.path.exists('vehicle_listings'):
        os.makedirs('vehicle_listings')
    if not os.path.exists(f'vehicle_listings/{listing_name}'):
        os.makedirs(f'vehicle_listings/{listing_name}')
    if not os.path.exists(f'vehicle_listings/{listing_name}/images'):
        os.makedirs(f'vehicle_listings/{listing_name}/images')
    for img in image_tags:
        img_url = img['src']
        # Only download images where the href starts with /inventoryphotos
        if img_url.startswith('/inventoryphotos'):
            if img_url.startswith('/'):
                img_url = base_url + img_url
            response = requests.get(img_url, stream=True)
            with open(f'vehicle_listings/{listing_name}/images/{img["alt"]}.png', 'wb') as out_file:
                out_file.write(response.content)

    print("Exiting download_images function")

def extract_vehicle_price(html_file):
    print("Entering extract_vehicle_price function")
    
    html_content = html_file

    soup = BeautifulSoup(html_content, 'html.parser')
    vehicle_price_div = soup.find('div', {'class': 'vehiclePricingHighlight featuredPrice'})

    vehicle_price = None
    if vehicle_price_div:
        vehicle_price_span = vehicle_price_div.find('span', {'class': 'vehiclePricingHighlightAmount'})
        if vehicle_price_span:
            vehicle_price = vehicle_price_span.text.strip()

    print("Exiting extract_vehicle_price function")
    return vehicle_price

def extract_vehicle_name(html_file):
    print("Entering extract_vehicle_name function")
   
    html_content = html_file

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


def extract_vehicle_info(html_file):
    print("Entering extract_vehicle_info function")
    
    ul_element = html_file

    soup = BeautifulSoup(ul_element, 'html.parser')
    info_items = soup.find_all('li', class_='info__item')

    vehicle_info = {}

    for item in info_items:
        label = item.find('span', class_='info__label').text.strip()
        value = item.find('span', class_='info__value')
        if value:
            vehicle_info[label] = value.get('title', '').strip()

    print("Exiting extract_vehicle_info function")
    return vehicle_info

def main():
    driver_path = 'chromedriver.exe'
    page_url = "https://www.pinkertonlynchburg.com/new-trucks.html?pt=1"


    
    while page_url:
        html_contents, page_url = scrape_links_and_download_html(driver_path, page_url)

        for html_content in html_contents:
            features = extract_vehicle_features(html_content)
            price = extract_vehicle_price(html_content)
            name = extract_vehicle_name(html_content)
            vehicle_info = extract_vehicle_info(html_content)

            # Create a Vehicle object
            vehicle = Vehicle(features, vehicle_info, price, name, [], html_content)

            # Download images
            download_images(html_content, name)

            # Write the vehicle attributes to a JSON file
            with open(f'vehicle_listings/{name}/attributes.json', 'w') as json_file:
                json.dump(vehicle.__dict__, json_file)


if __name__ == "__main__":

    main()



#TO-DO:
#Scrape: MPG, Car title, vehicle information, price, and the pictures
#then we need to categorize these features into the facebook features
