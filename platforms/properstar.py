from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class Properstar:
    def __init__(self, city, min_price=None, max_price=None, bedrooms=None, property_type=None):
        self.city = city
        self.min_price = min_price
        self.max_price = max_price
        self.property_type = property_type
        self.bedrooms = bedrooms
        
    
    def build_city(self):
        city = f"spanje/{self.city}"
        return city

    def build_url(self):
        base_url = f"https://www.properstar.nl/{self.build_city()}/huur"

        if self.property_type == 'apartment':
            base_url += "/appartement-huis"
        elif self.property_type == 'room':
            base_url += "/kamer"

        params = {}

        if self.min_price:
            params['price.min'] = self.min_price
        if self.max_price:
            params['price.max'] = self.max_price

        if self.bedrooms and self.property_type == 'apartment':
            base_url += f"/{self.bedrooms}p-slaapkamers"

        query_string = urlencode(params)
        full_url = f"{base_url}?{query_string}" if query_string else base_url
        return full_url
    
    def get_listing_urls(self):
        url = self.build_url()
        print(f"Scraping from: {url}")

        driver = webdriver.Chrome()
        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'container')))

            listings = driver.find_elements(By.CSS_SELECTOR, 'article.item-adaptive.card-extended')

            urls = []

            for listing in listings[:5]:
                link_tag = listing.find_element(By.TAG_NAME, 'a')
                link_url = f"{link_tag.get_attribute('href')}"
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
                
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.itemdetails-list.pane1')))

                title = driver.find_element(By.CSS_SELECTOR, 'div.main-info').text
                
                 # Extracting and processing the price
                price_elements = driver.find_element(By.CSS_SELECTOR, 'div.listing-info-price.h2').text.split('\n')
                price = ' '.join(price_elements) if isinstance(price_elements, list) else price_elements

                size_elements = driver.find_element(By.CSS_SELECTOR, 'div.highlights').text.split(' • ')
                size = ' '.join(size_elements) if isinstance(size_elements, list) else size_elements
                
                data.append((title, price, size, url))
                
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error while scraping {url}: {e}")
            data.append('N/A')
        finally:
            driver.quit()

        return data