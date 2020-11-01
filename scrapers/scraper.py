from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

CHROME_DRIVERS = "./chromedriver"


def getDriver():
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    # initialize driver
    driver = webdriver.Chrome(
        executable_path=CHROME_DRIVERS, chrome_options=options)
    return driver


def connectToBase(browser, baseUrl):
    base_url = baseUrl
    connection_attempts = 0
    while connection_attempts < 3:
        try:
            browser.get(base_url)
            WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            return True
        except Exception as e:
            print(e)
            connection_attempts += 1
            print(f"Error connecting to {base_url}.")
            print(f"Attempt #{connection_attempts}.")
    return False


def getUrls(html):
    parser = 'html.parser'
    urls = []
    try:
        soup = BeautifulSoup(html, parser)
        for link in soup.find_all('a', href=True):
            urls.append(link['href'])
    except:
        pass
    return urls
