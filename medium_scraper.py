import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


##-------------------##
# Webdriver options
##-------------------##

def connect_chrome():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('log-level=3')
    options.add_argument("--incognito")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    time.sleep(2)
    return driver

##-------------------##
# Publications
##-------------------##

urls = {
    'Towards Data Science': 'https://towardsdatascience.com/archive/{0}/{1:02d}/{2:02d}',
    'UX Collective': 'https://uxdesign.cc/archive/{0}/{1:02d}/{2:02d}',
    'The Startup': 'https://medium.com/swlh/archive/{0}/{1:02d}/{2:02d}',
    'The Writing Cooperative': 'https://writingcooperative.com/archive/{0}/{1:02d}/{2:02d}',
    'Data Driven Investor': 'https://medium.com/datadriveninvestor/archive/{0}/{1:02d}/{2:02d}',
    'Better Humans': 'https://medium.com/better-humans/archive/{0}/{1:02d}/{2:02d}',
    'Better Marketing': 'https://medium.com/better-marketing/archive/{0}/{1:02d}/{2:02d}',
}

##-------------------##
# Auxiliary functions
##-------------------##

def is_leap(year):
    if year % 4 != 0:
        return False
    elif year % 100 != 0:
        return True
    elif year % 400 != 0:
        return False
    else:
        return True
    
def convert_day(day, year):
    month_days = [31, 29 if is_leap(year) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    m = 0
    d = 0
    while day > 0:
        d = day
        day -= month_days[m]
        m += 1
    return (m, d)

def get_claps(claps_str):
    if (claps_str is None) or (claps_str == '') or (claps_str.split is None):
        return 0
    split = claps_str.split('K')
    claps = float(split[0])
    claps = int(claps*1000) if len(split) == 2 else int(claps)
    return claps

def get_img(img_url, dest_folder, dest_filename):
    ext = img_url.split('.')[-1]
    if len(ext) > 4:
        ext = 'jpg'
    dest_filename = f'{dest_filename}.{ext}'
    with open(f'{dest_folder}/{dest_filename}', 'wb') as f:
        f.write(requests.get(img_url, allow_redirects=False).content)
    return dest_filename



data = []

##-------------------##
# Scraping function
##-------------------##

def scrape_medium(number_of_days=365, years=[2018, 2019, 2020, 2021, 2022], n_save=0, save_frequency=100):

    ## We iterate through the years

    for year in years:

        ## Random sampling of days without replacement

        selected_days = random.sample([i for i in range(1, 367 if is_leap(year) else 366)], number_of_days)

        article_id = 0
        i = 0
        n = len(selected_days)

        for d in selected_days:
            i += 1
            month, day = convert_day(d, year)
            date = '{0}-{1:02d}-{2:02d}'.format(year, month, day)
            print(f'{i} / {n} ; {date}')


            ## Get all articles for that date and publication

            for publication, url in urls.items():
                response = requests.get(url.format(year, month, day), allow_redirects=True)
                if not response.url.startswith(url.format(year, month, day)):
                    continue
                soup = BeautifulSoup(response.content, 'html.parser')
                articles = soup.find_all("a")
                articles = [article for article in articles if "Read more…" in article.text.strip()]

                ## Scrape articles

                if len(articles) > 0:
                    for item in articles:
                        try:
                            browser = connect_chrome()
                            browser.get(item['href'])
                            time.sleep(3)

                            try:
                                title = browser.find_element(By.XPATH, "//h1")
                            except:
                                break
                            title = title.text
                            article_id += 1
                            article_text = []
                            try:
                                v = browser.find_element(By.XPATH, "//*[@id=\"root\"]/div/div[3]/div/div/main/div/div[3]/div[1]/div/article/div/div[2]/section")
                            except:
                                break
                            v = v.find_elements(By.XPATH, './/p')
                            for n in v:
                                article_text.append(n.text)
                            article_text = '[SEP]'.join(article_text)
                            article_text = article_text.strip()
                            try:
                                claps = browser.find_element(By.XPATH, "//*[@id=\"root\"]/div/div[3]/div/div/main/div/div[3]/footer/div/div/div/div/div[1]/div[1]/span[1]/div/div[2]/div/div/p/button")
                            except:
                                break
                            claps = get_claps(claps.text)

                            # Create csv file
                            data.append([article_id, title, article_text, claps, publication, year])
                            if len(data) == save_frequency:
                                n_save = n_save + len(data)
                                medium_df = pd.DataFrame(data, columns=['id', 'title', 'text', 'claps', 'publication', 'year'])
                                medium_df.to_csv('C:\\py\\boost project\\medium_all\\medium_' + str(n_save) + '.csv', index=False)
                                data = []
                        except:
                            pass

            #Sleep for a few seconds so we don't get banned

            time.sleep(random.randint(3,8))
        time.sleep(random.randint(3,8))


if __name__ == "__main__":
    scrape_medium()