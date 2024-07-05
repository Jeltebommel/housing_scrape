from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class Casamona:
    def __init__(self, city, min_price=None, max_price=None, bedrooms=None):
        self.city = city
        self.min_price = min_price
        self.max_price = max_price
        self.bedrooms = bedrooms

    def build_city(self):
        city = f"_city:{self.city}"
        return city

    def build_url(self):
        base_url = f"https://www.casamona.com/en/for-rent/{self.build_city()}"
        params = {}

        if self.min_price:
            params['pricemin'] = self.min_price
        if self.max_price:
            params['pricemax'] = self.max_price
        if self.bedrooms:
            params['rooms'] = self.bedrooms

        param_str = ",".join([f"{key}:{value}" for key, value in params.items()])
        full_url = f"{base_url},{param_str},mode:mosaic,d:created-desc,p:1/" if param_str else f"{base_url},mode:mosaic,d:created-desc,p:1/"
        return full_url

    def get_listing_urls(self):
        url = self.build_url()
        print(f"Scraping from: {url}")

        driver = webdriver.Chrome()
        driver.get(url)

        try:
            
            WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'main.col')))
            time.sleep(10)
            listings = driver.find_elements(By.CSS_SELECTOR, 'div.property-list-item.col')

            urls = []

            for listing in listings[:5]:
                link_tag = listing.find_element(By.CSS_SELECTOR, 'a.add-to-fav')
                link_url = link_tag.get_attribute('data-url')
                urls.append(link_url)

            return urls
        except TimeoutException:
            print(f"Timeout while loading main page {url}")
            return []
        except Exception as e:
            print(f"Error while scraping main page {url}: {e}")
            return []
        finally:
            driver.quit()

    def scrape(self):
        urls = self.get_listing_urls()

        data = []

        driver = webdriver.Chrome()
        
        try:
            for url in urls:
                driver.get(url)
                
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

                title = driver.find_element(By.CSS_SELECTOR, 'header.mr-2 h1').text

                price = driver.find_element(By.CSS_SELECTOR, 'span.h4.m-0.align-middle').text

                size = driver.find_element(By.CSS_SELECTOR, 'ul.property-features').text
                
                
                data.append((title, price, size, url))
                
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error while scraping {url}: {e}")
            data.append('N/A')
        finally:
            driver.quit()

        return data