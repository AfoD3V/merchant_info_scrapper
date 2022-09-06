import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod


class Scrapper(ABC):
    @abstractmethod
    def __init__(self):
        # URL of site where do want to proceed scrap
        self.url = "https://lostmerchants.com/"
        self.region = "region_name"
        self.server = "server_name"

    @abstractmethod
    def scrape_data(self):
        pass


class EuProcyonScraper(Scrapper):
    def __init__(self):
        # URL of site where do want to proceed scrap
        self.url = "https://lostmerchants.com/"
        self.region = "EU Central"
        self.server = "Procyon"

    def scrape_data(self) -> str:
        # Chrome settings
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")

        # URL and driver settings
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(self.url)

        # Waiting for drop_down menu content to load
        driver.implicitly_wait(5)

        # Region selection if not set in params than going "EU central" by default
        region = driver.find_element(By.ID, 'severRegion')
        drp_region = Select(region)
        drp_region.select_by_visible_text(self.region)

        # Server selection if not set in params than going "Procyon" by default
        server = driver.find_element(By.ID, 'server')
        drp_region = Select(server)
        drp_region.select_by_visible_text(self.server)

        # Sleep time for rest of dynamically generated content to load in
        time.sleep(5)

        # Parsing html
        soup = BeautifulSoup(driver.page_source, 'lxml')

        return str(soup)




scrappy = EuProcyonScraper()
data = scrappy.scrape_data()
print(type(data))
