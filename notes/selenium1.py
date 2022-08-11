from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import sys

import time
from woocommerce import API


consumer_key = "ck_88dd11b57062ee98fd6cd270fa115fe88e03e04f"

consumer_secret = "cs_8ab6edb8afcbfc49c3acd66513345bb97ca8db64"


class ProductWB:
    def __init__(self, url):
        self.success_post_count = 0
        self.all_post_count = 0
        self.url = url

    def add_to_wp(self, pr):
        wcapi = API(
            url="https://3.kpipartners.ru", #link to wordpress's site
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            timeout=2500,
        )
        for i in pr:
            response = wcapi.post("products", i)
            status = response.status_code
            if status >= 400:
                time.sleep(50)
                response = wcapi.post("products", i)
                print(response)
            else:
                print(response)



    def parse_product(self, page=0):
        try:
            while True:
                page += 1
                batch = []
                if '&' in self.url[self.url.find('page=')+5:]:
                    next = self.url[self.url.find('page=')+5:].find('&')
                    driver.get(self.url[:self.url.find('page=')+5]+str(page)+self.url[next:])
                else:
                    driver.get(self.url[:self.url.find('page=')+5]+str(page))
                
                try:
                  if 'Что-то пошло не так' in driver.find_element(By.XPATH, '//*[@id="error500"]/div/div/h1)').text:
                    print("restart script or page on Google or url doesn't exist")
                    driver.quit()
                except:
                  pass

                time.sleep(10)
                driver.refresh()
                
                WebDriverWait(driver, timeout=30).until(EC.presence_of_element_located((By.CLASS_NAME, "product-card__main.j-card-link")))

                product_card = driver.find_elements(By.CLASS_NAME, value="product-card__img-wrap.img-plug.j-thumbnail-wrap")
                price = driver.find_elements(By.CLASS_NAME, value="lower-price")
                links = [i.get_attribute('href') for i in driver.find_elements(By.CLASS_NAME, value="product-card__main.j-card-link")]

                for i in range(len(product_card)):
                  img = product_card[i].find_element(By.TAG_NAME, 'img')
                  title = img.get_attribute('alt')
                  batch.append({"name": title})

                for pr in range(len(price)):
                  batch[pr]["regular_price"] = price[pr].text

                for link in range(len(links)):
                  driver.get(links[link])
                  WebDriverWait(driver, timeout=50).until(EC.presence_of_element_located((By.CLASS_NAME, "collapsable__content.j-description")))
                  descrip = driver.find_element(By.CLASS_NAME, value="collapsable__content.j-description").find_element(By.TAG_NAME, 'p').text
                  img = driver.find_element(By.CLASS_NAME, 'swiper-wrapper').find_elements(By.TAG_NAME, 'img')
                  images = []
                  for i in img:
                    images.append({"src": i.get_attribute('src')})
                  batch[link]["description"] = descrip
                  batch[link]["images"] = images
                self.add_to_wp(batch)
        except:
            pass



if __name__ == "__main__":
    print("Введите ссылку для парсинга")
    #url = str(input())
    url = "https://www.wildberries.ru/seller/25172?&page=1"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    
    if 'page=' not in url:
        if '?&' not in url:
            url += '?&page=1'
        else:
            url += 'page=1'
    if 'seller' in url or 'brand' in url:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        WebDriverWait(driver, timeout=30).until(EC.presence_of_element_located((By.CLASS_NAME, "product-card__main.j-card-link")))
        product_class_object = ProductWB(url=url)
        print(product_class_object.parse_product())
    else:
        print("this is not seller's page")
