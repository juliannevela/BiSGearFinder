"""
This module uses Selenium to interact with the WowHead website.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

BIS_GEAR_FINDER = {}

# Configure Firefox profile with custom preferences
firefox_profile = FirefoxProfile()
firefox_profile.set_preference("permissions.default.image", 2)

# Configure Firefox options with custom profile and driver settings
options = Options()
options.add_argument("-headless")
options.profile = firefox_profile

# Start the driver
browser = webdriver.Firefox(options=options)
browser.get("https://www.wowhead.com/guide/classes/death-knight/frost/bis-gear")

# Wait for page to render fully, then store page source for processing
page_loaded = WebDriverWait(driver=browser, timeout=5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#guide-body"))
)
page = browser.page_source

# Parse the information received by the browser using BeautifulSoup
soup = BeautifulSoup(page, "lxml")
gear_table = soup.select("#guide-body > div.wh-center > table > tbody")
header = []
rows = []
for i, row in enumerate(gear_table[0].find_all("tr")):
    if i == 0:
        header = [el.text.strip() for el in row.find_all("td")]
    else:
        rows.append([el.text.strip() for el in row.find_all("td")])
print(header)
for row in rows:
    print(row)

# Exit the instance of the webdriver
browser.quit()
