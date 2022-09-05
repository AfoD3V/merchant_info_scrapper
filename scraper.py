import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self, url: str = "https://lostmerchants.com/"):
        # URL of site where do want to proceed scrap
        self.url = url

    def scrape_data(self, region_name: str = "EU Central", server_name: str = "Procyon"):
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
        drp_region.select_by_visible_text(region_name)

        # Server selection if not set in params than going "Procyon" by default
        server = driver.find_element(By.ID, 'server')
        drp_region = Select(server)
        drp_region.select_by_visible_text(server_name)

        # Sleep time for rest of dynamically generated content to load in
        time.sleep(5)

        # Parsing html
        soup = BeautifulSoup(driver.page_source, 'lxml')

        return str(soup)


class FileCreator:

    def __init__(self, html_data):
        self.data = html_data
        self.data_path = 'work_files/csv_data.csv'

    def create_csv_file(self):
        # Data frame for further csv file
        df = pd.read_html(self.data)
        df[0].to_csv(self.data_path)

    def format_csv_file(self):
        with open(self.data_path, 'w') as f:
            for line in f:
                if 150 < len(line) < 400:
                    print(line)


scrappy = Scraper()
data = scrappy.scrape_data()

file = FileCreator(data)
file.create_csv_file()
file.format_csv_file()
