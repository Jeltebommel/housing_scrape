from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time



class Fotocasa:
    def __init__(self, city, min_price=None, max_price=None, bedrooms=None):
        self.city = city
        self.min_price = min_price
        self.max_price = max_price
        self.bedrooms = bedrooms

    def build_url(self):
        base_url = f"https://www.fotocasa.es/en/rental/homes/{self.city}/all-zones/"
        params = {}

        if self.min_price:
            params['minPrice'] = self.min_price
        if self.max_price:
            params['maxPrice'] = self.max_price
        if self.bedrooms:
            if self.bedrooms == "exactly_2":
                base_url += "2-rooms/"
            else:
                params['minRooms'] = self.bedrooms

        query_string = urlencode(params)
        full_url = f"{base_url}l" if not query_string else f"{base_url}l?{query_string}"
        
        return full_url
    
    def get_listing_urls(self):
        url = self.build_url()
        print(f"Scraping from: {url}")

        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(10)

        try:
            WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'section.re-SearchResult')))

            #urls = []

            listings = driver.find_elements(By.CSS_SELECTOR, 'section.re-SearchResult')
            for results in listings:
                results = results.text


            #for listing in listings:
                
                #link_tag = listing.find_element(By.TAG_NAME, 'a')
                #link_url = f"{link_tag.get_attribute('href')}"
                #urls.append(link_url)


            return results
        except TimeoutException:
            print(f"Timeout while loading main page {url}")
            return []
        except Exception as e:
            print(f"Error while scraping main page {url}: {e}")
            return []
        finally:
            driver.quit()


# Example usage:
fotocasa = Fotocasa(city="barcelona-capital", min_price=600, max_price=1800, bedrooms=2)
print(fotocasa.get_listing_urls())



