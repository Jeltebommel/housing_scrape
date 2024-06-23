from datetime import datetime, timedelta
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

    def build_url(self):
        base_url = f'https://housinganywhere.com/s/{self.city}--Spain'
        params = []

        if self.min_price:
            params.append(f'priceMin={self.min_price}')

        if self.max_price:
            params.append(f'priceMax={self.max_price}')

        if self.property_type:
            property_type_mapping = {
                'apartment': 'apartment-for-rent',
                'studio': 'studio-for-rent',
                'room': 'room-for-rent',
                'student_residence': 'student-residence-for-rent'
            }
            params.append(f'categories={property_type_mapping.get(self.property_type, self.property_type)}')

        if self.bedrooms:
            if self.bedrooms == '3+':
                params.append('bedroomCount=1,2,3,4+')
            else:
                params.append(f'bedroomCount={self.bedrooms}')

        query_string = '&'.join(params)
        full_url = f'{base_url}?{query_string}'
        return full_url

    def scrape_listing_details(self, driver, url):
        driver.get(url)
        try:
            # Wait until the page is fully loaded
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-md-8.css-1wlzjv3')))

            # Extract data
            title = driver.find_element(By.CSS_SELECTOR, 'span[data-test-locator="Listing/ListingInfo/street"]').text

            # Extract monthly price
            # Extract price
            outer_container = driver.find_element(By.CSS_SELECTOR, 'div.css-2iqnx5-listingInfo')
            
            second_div = outer_container.find_elements(By.TAG_NAME, 'div')
            for each in second_div:
                try:
                    price_text = each.find_element(By.CSS_SELECTOR, 'span[data-test-locator="Listing/ListingInfo/Price"]').text
                    break 
                except NoSuchElementException:
                    continue 
            

            # Extract property size
            size_text = driver.find_element(By.CSS_SELECTOR, 'div.MuiChip-root[data-test-locator="HighlightsTags/Property"]').text
            size = size_text.split(': ')[1]  # Get the size part

            return (title, price_text, size, url)
        
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
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'body')))
            time.sleep(5)  # Ensure all elements are loaded

            # check the page source to see if the landingpage is a captcha
            #page_source = driver.page_source
            #print("Page Source:")
            #print(page_source)

            # Extract listing URLs
            listings = driver.find_elements(By.CSS_SELECTOR, 'div.css-wp5dsn-container')
            urls = []
            for listing in listings:
                link_tags = listing.find_elements(By.TAG_NAME, 'a')
                for link_tag in link_tags:
                    link_url = link_tag.get_attribute('href')
                    if link_url:
                        urls.append(link_url)

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

# Usage example
housing_anywhere = HousingAnywhere(city='Barcelona', min_price=1000, max_price=None, property_type='apartment', bedrooms='2')
data = housing_anywhere.scrape()
print(data)
