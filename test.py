import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_links_and_download_html(driver_path, page_url):
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get(page_url)

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
                print(f"HTML file for {link} already exists. Skipping download.")
                continue

            driver.get(link)
            html_content = driver.page_source

            if not html_content:
                print("No HTML content found for the current page.")
            else:
                html_contents.append(html_content)

    if not html_contents:
        print("No HTML contents to write to files.")
    else:
        # Create a directory for the downloaded HTML files if it doesn't exist
        if not os.path.exists('downloaded_html_files'):
            os.makedirs('downloaded_html_files')

        for i, content in enumerate(html_contents, start=1):
            with open(f'downloaded_html_files/linked_page_{i}.html', 'w', encoding='utf-8') as file:
                file.write(content)

    driver.quit()
    return html_contents

def extract_vehicle_features(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    vehicle_highlights_list = soup.find('ul', {'id': 'vehicle-highlights-list'})

    vehicle_features = []
    if vehicle_highlights_list:
        vehicle_highlights_items = vehicle_highlights_list.find_all('li')
        for item in vehicle_highlights_items:
            feature_label = item.find('span')
            if feature_label:
                vehicle_features.append(feature_label.text.strip())

    return vehicle_features


def extract_vehicle_price(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    vehicle_price_div = soup.find('div', {'class': 'vehiclePricingHighlight featuredPrice'})

    vehicle_price = None
    if vehicle_price_div:
        vehicle_price_span = vehicle_price_div.find('span', {'class': 'vehiclePricingHighlightAmount'})
        if vehicle_price_span:
            vehicle_price = vehicle_price_span.text.strip()

    return vehicle_price

def extract_vehicle_name(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    vehicle_name_h2 = soup.find('h2', {'class': 'vehicle-title__text'})

    vehicle_name = None
    if vehicle_name_h2:
        vehicle_name_span = vehicle_name_h2.find('span', {'class': 'vehicle-title__year-make-model'})
        if vehicle_name_span:
            vehicle_name = vehicle_name_span.text.strip()

    return vehicle_name

def main():
    #driver_path = 'chromedriver.exe'
    #page_url = "https://www.pinkertonlynchburg.com/new-trucks.html"
    #html_contents = scrape_links_and_download_html(driver_path, page_url)
    # Test the first HTML file
    #if html_contents:
        first_html_file = 'downloaded_html_files/linked_page_1.html'
        features = extract_vehicle_features(first_html_file)
        print(features)

if __name__ == "__main__":
    main()


#TO-DO:
#Scrape: MPG, Car title, vehicle information, price
#then we need to categorize these features into the facebook features
