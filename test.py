from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from time import sleep
import requests
import quickstart
import re
from translate import Translator
import get_latitude_and_longitude



# Create a Translator object and translate the string
translator = Translator(to_lang="en")
driver = webdriver.Chrome()    
driver.maximize_window()
driver.get("https://www.byggmakker.no/kategori/trelast/terrassebord")

click_button = WebDriverWait(d, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "img[class\"product-card__carousel-image ls-is-cached lazyloaded\"]"))).click()