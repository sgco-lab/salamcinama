import os
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def setup_chrome():
    # نصب گوگل کروم (در اولین اجرای اسکریپت)
    subprocess.run("apt-get update", shell=True)
    subprocess.run("apt-get install -y google-chrome-stable", shell=True)

def run_scraper():
    setup_chrome()

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = "/usr/bin/google-chrome"  # مسیر Chrome در Linux

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    # ادامه اسکریپت...

if __name__ == "__main__":
    run_scraper()
