from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class RealEstate:
    def __init__(self, city, min_price=None, max_price=None, bedrooms=None):
        self.city = city
        self.min_price = min_price
        self.max_price = max_price
        self.bedrooms = bedrooms
        
    def build_city(self):
        city = f"{self.city.capitalize()}--spain"
        return city

    def build_url(self):
        base_url = f"https://www.realestate.com.au/international/es/{self.build_city()}/rent"
        params = {}

        if self.min_price:
            params['minprice'] = self.min_price
        if self.max_price:
            params['maxprice'] = self.max_price
        if self.bedrooms:
            params['minbed'] = self.bedrooms

        query_string = urlencode(params)
        full_url = base_url if not query_string else f"{base_url}?{query_string}"
        
        return full_url


    def get_listing_urls(self):
        url = self.build_url()
        print(f"Scraping from: {url}")

        driver = webdriver.Chrome()
        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.o8y0h-0.hxCDMi')))

            listings = driver.find_elements(By.CSS_SELECTOR, 'div.sc-1dun5hk-0.cOiOrj')

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
                
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

                title = driver.find_element(By.CSS_SELECTOR, 'h1.display-address').text

                price = driver.find_element(By.CSS_SELECTOR, 'div.sc-10v3xoh-0.kgiZMN.property-price').text.split(' ')[1]

                size = driver.find_element(By.ID, 'listing-features').text
                
                
                data.append((title, price, size, url))
                
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error while scraping {url}: {e}")
            data.append('N/A')
        finally:
            driver.quit()

        return data