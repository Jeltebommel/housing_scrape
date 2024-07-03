from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class HousingAnywhere:
    def __init__(self, city, min_price, max_price, property_type, bedrooms):
        self.city = city
        self.min_price = min_price
        self.max_price = max_price
        self.property_type = property_type
        self.bedrooms = bedrooms

    def build_city(self):
        city = f"{self.city.capitalize()}--Spain"
        return city
    
    def build_url(self):
        # Base URL
        base_url = f'https://housinganywhere.com/s/{self.build_city()}'
        
        # Create the parameters list
        params = []

        if self.min_price is not None:
            params.append(f'priceMin={self.min_price}00')
        
        if self.max_price is not None:
            params.append(f'priceMax={self.max_price}00')
        
        if self.property_type:
            if self.property_type == 'apartment':
                if self.bedrooms == '1':
                    base_url += '/one-bedroom-apartments'
                elif self.bedrooms == '2':
                    base_url += '/two-bedroom-apartments'
                elif self.bedrooms == '1or2':
                    params.append('bedroomCount=1%2C2&categories=apartment-for-rent')
                elif self.bedrooms == '3':
                    params.append('bedroomCount=3&categories=apartment-for-rent')
                elif self.bedrooms == '4+':
                    params.append('bedroomCount=4%2B&categories=apartment-for-rent')
                else:
                    params.append('bedroomCount=1%2C2%2C3%2C4%2B&categories=apartment-for-rent')
            elif self.property_type == 'studio':
                base_url += '/studio-for-rent'
            elif self.property_type == 'room':
                base_url += '/private-rooms'
        
        # Join the parameters with '&' and add to the URL
        query_string = '&'.join(params)
        full_url = f'{base_url}?{query_string}'
        
        return full_url

    def scrape_listing_details(self, driver, url):
        driver.get(url)
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-md-8.css-1wlzjv3')))

            # Extract title
            title = driver.find_element(By.CSS_SELECTOR, 'span[data-test-locator="Listing/ListingInfo/street"]').text

            # Extract price
            price_element = driver.find_element(By.CSS_SELECTOR, 'div.listing-info-price.h2')
            price = price_element.text if price_element else 'N/A'

            # Extract size
            size_text = driver.find_element(By.CSS_SELECTOR, 'div.MuiChip-root[data-test-locator="HighlightsTags/Property"]').text
            size = size_text.split(': ')[1] if size_text else 'N/A'

            return (title, price, size, url)
        
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error while scraping {url}: {e}")
            return ('N/A', 'N/A', 'N/A', url)

    def scrape(self):
        url = self.build_url()
        print("Scraping URL:", url)

        driver = webdriver.Chrome()
        driver.get(url)

        try:
            # Wait for the listings to load
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.item-page.listing-page')))
            time.sleep(5)  # Ensure all elements are loaded

            # Extract listing URLs
            listings = driver.find_elements(By.CSS_SELECTOR, 'div.item-page.listing-page')
            urls = [listing.find_element(By.TAG_NAME, 'a').get_attribute('href') for listing in listings]

            # Scrape details for each listing
            data = []
            for url in urls:
                listing_details = self.scrape_listing_details(driver, url)
                data.append(listing_details)

            return data
        except TimeoutException:
            print(f"Timeout while loading main page {url}")
            return []
        except Exception as e:
            print(f"Error while scraping main page {url}: {e}")
            return []
        finally:
            driver.quit()

# Example usage:
if __name__ == "__main__":
    housinganywhere = HousingAnywhere(city='barcelona', min_price='500', max_price='3000', property_type='apartment', bedrooms=None)
    results = housinganywhere.scrape()
    print(results)
