# import os
# from pathlib import Path
# from time import sleep

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service

# ROOT_PATH = Path(__file__).parent.parent
# CHROME_DRIVER_NAME = "chromedriver.exe"
# CHROME_DRIVER_PATH = ROOT_PATH / "bin" / CHROME_DRIVER_NAME


# def make_chrome_browser(*options):
#     chrome_options = webdriver.ChromeOptions()

#     if options is not None:
#         for option in options:
#             chrome_options.add_argument(option)

#     if os.environ.get("SELENIUM_HEADLESS") == "1":
#         chrome_options.add_argument("--headless")

#     chrome_service = Service(executable_path=CHROME_DRIVER_PATH)
#     browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
#     return browser


# if __name__ == "__main__":
#     browser = make_chrome_browser("--headless")
#     browser.get("https://www.google.com.br/")
#     sleep(5)


import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()

    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    if os.environ.get("SELENIUM_HEADLESS") == "1":
        chrome_options.add_argument("--headless=new")

    # Sem o parâmetro executable_path, o Selenium Manager identifica a versão
    # instalada do Chrome (153+) e obtém o driver compatível automaticamente
    chrome_service = Service()
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser


if __name__ == "__main__":
    browser = make_chrome_browser("--headless=new")
    browser.get("https://www.google.com.br/")
    sleep(5)
