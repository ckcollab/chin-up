from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from polished.backends import DjangoBackend
from polished.decorators import polish


class ChinupDjangoBackend(DjangoBackend):
    pass
