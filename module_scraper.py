"""Scrapper for collecting data from website

This module allow user to get data from website which is covering location
and items which specified merchant is holding for-sell.

This module requires that `pandas`, 'selenium', 'webdriver_manager', 'bs4'
be installed within the Python environment you are running this module in.

This file can also be imported as a module and contains the following
functions:

    * EuProcyonScraper class which is providing function:
        scrape_data()
            Function is collecting full code from dynamically generated content
            and returning string object.

    * CsvFileCreator class which is providing function:
        create_file(scrapped_data: str)
            Function for creating csv file from scrapped data, parameter
            which is given for this method, should be provided by EuProcyonScraper
            instance with a use of scrape_data() method.
"""

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
        # Region and server for further scrap
        self.region = "region_name"
        self.server = "server_name"

    @abstractmethod
    def scrape_data(self):
        pass


class ScrapperSettings:
    """
    A class used for providing must settings for latter designed scrape classes

    ...

    Methods
    -------
    scraper_settings(url, region_name, server_name)
        Providing static method which is used mainly for giving all the settings
        inside later scrapper classes.

    """

    @staticmethod
    def scraper_settings(url, region_name, server_name):
        """
        Providing static method which is used mainly for giving all the settings
        inside later scrapper classes.

        Parameters
        ----------
        url : str
            URL of site we want to scrape
        region_name : str
            One of the regions which can be picked from drop down list on site
        server_name : str
            One of the servers which can be picked from drop down list on site

        Returns
        -------
        str
            str object created with a use of bs4
        """
        # Chrome settings
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")

        # URL and driver settings
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(url)

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


class EuProcyonScraper(Scrapper):
    """
        A class designed for scrapping data from concrete on web region / server ->
        EuCentral / Procyon.

        ...

        Methods
        -------
        scrape_data()
            Scrapping data from site and returning string object.
    """

    def __init__(self):
        # URL of site where do want to proceed scrap
        self.url = "https://lostmerchants.com/"
        self.region = "EU Central"
        self.server = "Procyon"

    def scrape_data(self) -> str:
        """Scraping data from site and returning str object

        Returns
        -------
        str
            Soup object converted into string
        """
        # instance of settings class
        settings = ScrapperSettings()
        soup_string = settings.scraper_settings(self.url, self.region, self.server)

        return soup_string


class FileCreator(ABC):
    @abstractmethod
    def __init__(self):
        # Path for file creation
        file_type = 'file_type'
        self.data_path = f'work_files/{file_type}_file.{file_type}'

    @abstractmethod
    # Method to make csv_file from scrapped data
    def create_file(self, scrapped_data: str):
        pass


class CsvFileCreator(FileCreator):
    """
        A class which goal is to make CSV file from the scrapped data

        Methods
        -------
        create_file()
            Method for creating file
    """

    def __init__(self):
        # File type
        self.file_type = 'csv'
        # Path where file should be saved
        self.data_path = f'work_files/{self.file_type}_file.{self.file_type}'

    def create_file(self, scrapped_data: str):
        """Creating file of specified format

        Parameters
        ----------
        scrapped_data : str
            String object with code dynamically generated on site

        Raises
        ------
        TypeError
            If data provided is in format other than string.
        """

        # Check for the correctness of data
        if scrapped_data is not str:
            raise TypeError("Provided data must be a string")
        # Data frame for further csv file
        df = pd.read_html(scrapped_data)
        df[0].to_csv(self.data_path)


"""
Basic usage schema:

1. create any instance of scrapper
scrappy = EuProcyonScraper()

2. make a var to store scrapped data
data = scrappy.scrape_data()

3. Make a instance of file creator
csv_file = CsvFileCreator()

4. Create file
csv_file.create_file(data)
"""