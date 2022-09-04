import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self, url):
        self.url = url

    def scrape_data(self, region_name: str = "EU Central", server_name: str = "Procyon") -> str:

        # Chrome settings
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")

        # URL and driver settings
        url = 'https://lostmerchants.com/'
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(self.url)

        # Waiting for all content on page to load
        driver.implicitly_wait(5)

        # Region selection
        region = driver.find_element(By.ID, 'severRegion')
        drp_region = Select(region)
        drp_region.select_by_visible_text(region_name)

        # Server selection
        server = driver.find_element(By.ID, 'server')
        drp_region = Select(server)
        drp_region.select_by_visible_text(server_name)

        # Sleep time for rest of dynamically generated content to load in
        time.sleep(5)

        # Parsing html
        soup = BeautifulSoup(driver.page_source, 'lxml')

        return str(soup)


c = Scraper("https://lostmerchants.com/")
print(c.scrape_data())
