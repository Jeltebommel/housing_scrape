from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class ProperstarScraper:
    def __init__(self, city, min_price=None, max_price=None, bedrooms=None):
        self.city = city
        self.min_price = min_price
        self.max_price = max_price
        self.bedrooms = bedrooms

    def build_url(self):
        base_url = f"https://www.properstar.nl/spanje/{self.city}/huur/appartement-huis"
        params = {}

        if self.min_price:
            params['price.min'] = self.min_price
        if self.max_price:
            params['price.max'] = self.max_price
        if self.bedrooms:
            base_url += f"/{self.bedrooms}p-slaapkamers"

        query_string = urlencode(params)
        full_url = base_url if not query_string else f"{base_url}?{query_string}"
        
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

            for listing in listings:
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

# Example usage:
properstar_scraper = ProperstarScraper(city="barcelona", min_price=500, max_price=2000, bedrooms=2)
print(properstar_scraper.get_listing_urls())