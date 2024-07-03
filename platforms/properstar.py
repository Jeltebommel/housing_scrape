from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class Properstar:
    def __init__(self, city, min_price=None, max_price=None, bedrooms=None, property_type='apartments'):
        self.city = city
        self.min_price = min_price
        self.max_price = max_price
        self.bedrooms = bedrooms
        self.property_type = property_type
    
    def build_city(self):
        city = f"spanje/{self.city}"
        return city

    def build_url(self):
        base_url = f"https://www.properstar.nl/{self.build_city()}/huur"
        
        if self.property_type == 'room':
            base_url += "/kamer"
        else:
            base_url += "/appartement-huis"
            if self.bedrooms:
                base_url += f"/{self.bedrooms}p-slaapkamers"

        params = {}
        if self.min_price:
            params['price.min'] = self.min_price
        if self.max_price:
            params['price.max'] = self.max_price

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
                
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.item-page.listing-page')))

                title = driver.find_element(By.CSS_SELECTOR, 'div.main-info').text
                
                 # Extracting and processing the price
                price_elements = driver.find_element(By.CSS_SELECTOR, 'div.listing-info-price.h2').text.split('\n')
                price = ' '.join(price_elements) if isinstance(price_elements, list) else price_elements

                size = driver.find_element(By.CSS_SELECTOR, 'div.highlights').text.split(' • ')[4]
                
                data.append((title, price, size, url))
                
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error while scraping {url}: {e}")
            data.append('N/A')
        finally:
            driver.quit()

        return data

# Example usage:
if __name__ == "__main__":
    properstar = Properstar(city='barcelona', min_price='500', max_price='3000', bedrooms=None, property_type='room')
    results = properstar.build_url()
    print(results)