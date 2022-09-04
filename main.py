from selenium import webdriver
import chromedriver_autoinstaller
import os

chromedriver_autoinstaller.install()


chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")


driver = webdriver.Chrome()
driver.get("http://www.python.org")
print(driver.title)
