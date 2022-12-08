import re
import os.path
import time
import random
from bs4 import BeautifulSoup

from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import lib.config
import headers
from lib.csv_handler import CsvHandler