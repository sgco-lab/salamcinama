import os
import time
import zipfile
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pyvirtualdisplay import Display

def download_chrome():
    chrome_url = "https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/1153606/chrome-linux.zip"
    chrome_zip = "chrome-linux.zip"
    chrome_dir = "/tmp/chrome"

    if not os.path.exists(chrome_dir):
        urllib.request.urlretrieve(chrome_url, chrome_zip)
        with zipfile.ZipFile(chrome_zip, 'r') as zip_ref:
            zip_ref.extractall("/tmp/")
        os.rename("/tmp/chrome-linux", chrome_dir)
        os.remove(chrome_zip)
    return os.path.join(chrome_dir, "chrome")

def run_scraper():
    chrome_path = download_chrome()

    display = Display(visible=0, size=(1920, 1080))
    display.start()

    options = Options()
    options.binary_location = chrome_path
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get("https://salamcinama.ir/inplay")
    time.sleep(5)
    print("✅ صفحه باز شد.")
    driver.quit()
    display.stop()

if __name__ == "__main__":
    run_scraper()
