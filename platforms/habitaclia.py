from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class Habitaclia:
    def __init__(self, city, min_price=None, max_price=None, bedrooms=None):
        self.city = city
        self.min_price = min_price
        self.max_price = max_price
        self.bedrooms = bedrooms

    def build_city(self):
        city = f"alquiler-{self.city}"
        return city

    def build_url(self):
        base_url = f"https://www.habitaclia.com/{self.build_city()}.htm"
        params = {}

        if self.min_price:
            params['pmin'] = self.min_price
        if self.max_price:
            params['pmax'] = self.max_price
        if self.bedrooms:
            params['hab'] = self.bedrooms

        query_string = urlencode(params)
        full_url = f"{base_url}?{query_string}" if query_string else base_url
        return full_url
    
    def get_listing_urls(self):
        url = self.build_url()
        print(f"Scraping from: {url}")

        driver = webdriver.Chrome()
        driver.get(url)

        try:
            
            WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'article.js-list-item')))
            time.sleep(10)
            listings = driver.find_elements(By.CSS_SELECTOR, 'article.js-list-item')

            urls = []

            for listing in listings[:5]:
                link_url = listing.get_attribute('data-href')
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
    


# Example usage
city = 'barcelona'
min_price = '500'
max_price = '1500'
bedrooms = '2'

habitaclia = Habitaclia(city, min_price, max_price, bedrooms)
print(habitaclia.get_listing_urls()) 