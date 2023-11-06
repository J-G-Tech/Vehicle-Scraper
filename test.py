import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

def download_html(url):
    response = requests.get(url)
    with open('webpage.html', 'w') as file:
        file.write(response.text)



driver = webdriver.Chrome(executable_path='C:/Users/gavis/OneDrive/Desktop/Projects/Vehicl Scraper/Vehicle-Scraper/chromedriver.exe')
driver.get("https://www.pinkertonlynchburg.com/searchnew.aspx")

carousel_items = driver.find_elements(By.CLASS_NAME, "vehicle-image")

for item in carousel_items:
    item.click()
    download_html(driver.current_url)
