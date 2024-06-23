from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
from selenium_stealth import stealth
import pickle

class Idealista:
    def __init__(self, city, min_price=None, max_price=None, property_type=None, bedrooms=None):
        self.city = city
        self.min_price = min_price
        self.max_price = max_price
        self.property_type = property_type
        self.bedrooms = bedrooms

    def build_url(self):
        base_url = f'https://www.idealista.com/alquiler-viviendas/{self.city}/'
        params = []

        if self.max_price:
            params.append(f"con-precio-hasta_{self.max_price}")
        
        if self.min_price:
            params.append(f"precio-desde_{self.min_price}")

        if self.bedrooms:
            if self.bedrooms == '2':
                params.append('de-dos-dormitorios')
                params.append('de-tres-dormitorios')
                params.append('de-cuatro-cinco-habitaciones-o-mas')
            else:
                bedrooms_mapping = {
                    '1': 'de-un-dormitorio',
                    '3': 'de-tres-dormitorios',
                    '4': 'de-cuatro-dormitorios',
                    '5+': 'de-cinco-habitaciones-o-mas'
                }
                if self.bedrooms in bedrooms_mapping:
                    params.append(bedrooms_mapping[self.bedrooms])

        query_string = ','.join(params)
        full_url = f'{base_url}{query_string}/'
        
        return full_url


    def scrape(self):
        url = self.build_url()
        print("Scraping URL:", url)

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run Chrome in headless mode
        options.add_argument("start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])


        driver = webdriver.Chrome(options=options)
       
        driver.get(url)
        # Wait 3.5 on the webpage before trying anything 
        time.sleep(3.5)
        

        try:
            print("Waiting for elements to load...")
            WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'body')))
            print("Elements loaded successfully.")
            
            # Wait 3.5 on the webpage before trying anything 
            time.sleep(3.5)

            # check the page source to see if the landingpage is a captcha
            page_source = driver.page_source
            print("Page Source:")
            print(page_source)

            listings = driver.find_elements(By.CSS_SELECTOR, 'div.item-info-container ')
            print(f"This is what I found:  {listings}")
            #urls = []
            #for listing in listings[:10]:  # Limit to the first 10 listings
               # link_tag = listing.find_element(By.TAG_NAME, 'a')
                #link_url = f"https://www.idealista.com{link_tag.get_attribute('href')}"
                #urls.append(link_url)

            # Scrape details for each listing
            #data = []
            #for url in urls:
              #  listing_details = self.scrape_listing_details(driver, url)
              #  data.append(listing_details)

            return listings
        except TimeoutException:
            print(f"Timeout while loading main page: {url}")
            return []
        except NoSuchElementException as e:
            print(f"Element not found: {e}")
            return []
        except Exception as e:
            print(f"Error while scraping main page {url}: {e}")
            return []
        finally:
            driver.quit()

# Example usage
idealista = Idealista(
    city='barcelona-barcelona',
    min_price='500',
    max_price='1500',
    bedrooms='2'
)
data = idealista.scrape()
print("Scraped data:", data)


"""
    def scrape_listing_details(self, driver, url):
        driver.get(url)
        try:
            # Wait until the page is fully loaded
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

            # Extract data
            title = driver.find_element(By.CSS_SELECTOR, 'span.main-info__title-main').text
            price = driver.find_element(By.CSS_SELECTOR, 'span.info-data-price').text.strip()
            size = driver.find_element(By.CSS_SELECTOR, 'span.info-data-meter2').text.strip()

            features = driver.find_elements(By.CSS_SELECTOR, 'div.details-property_features li')
            features = [feature.text for feature in features]

            return (title, price, size, features, url)
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error while scraping {url}: {e}")
            return ('N/A', 'N/A', 'N/A', 'N/A', url)
"""