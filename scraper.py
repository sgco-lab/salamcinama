from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import os

def scrape():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get('https://salamcinama.ir/inplay')
    time.sleep(5)

    movies = driver.find_elements(By.CSS_SELECTOR, 'section.container.grid div.h-full')
    data = []
    for movie in movies:
        try:
            title_el = movie.find_element(By.CSS_SELECTOR, 'a.card-link')
            title = title_el.text.strip()
            poster = movie.find_element(By.TAG_NAME, 'img').get_attribute('src')
            director = movie.find_element(By.XPATH, './/span[contains(text(),"کارگردان")]/..').text.replace('کارگردان :','').strip()
            url = title_el.get_attribute('href')

            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(url)
            time.sleep(3)
            actors = ', '.join([el.text for el in driver.find_elements(By.CSS_SELECTOR, '.people-list li a')])
            summary = driver.find_element(By.CSS_SELECTOR, '.movie-content p').text.strip()
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            data.append({
                'title': title,
                'poster': poster,
                'director': director,
                'actors': actors,
                'summary': summary,
            })
        except Exception as e:
            print('Error scraping one movie:', e)

    driver.quit()
    return data

def render_html(data):
    os.makedirs('public', exist_ok=True)
    with open('public/index.html','w',encoding='utf-8') as f:
        f.write('<!DOCTYPE html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><title>در حال اکران</title><style>body{font-family:sans-serif;}.movie{display:flex;margin-bottom:20px;}.poster{width:150px;margin-left:10px;} .details{flex:1;}.title{font-size:1.5em;margin:0;} .small{color:#555;margin:5px 0;}</style></head><body>')
        f.write('<h1>فیلم‌های در حال اکران</h1>')
        for m in data:
            f.write(f'<div class="movie"><img class="poster" src="{m["poster"]}"/><div class="details"><h2 class="title">{m["title"]}</h2>')
            f.write(f'<p class="small"><strong>کارگردان:</strong> {m["director"]}</p>')
            f.write(f'<p class="small"><strong>بازیگران:</strong> {m["actors"]}</p>')
            f.write(f'<p>{m["summary"]}</p></div></div>')
        f.write('</body></html>')

def main():
    data = scrape()
    render_html(data)

if __name__ == '__main__':
    main()
