from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class HousingAnywhere:
    def __init__(self, city, min_price, max_price, bedrooms):
        self.city = city
        self.min_price = min_price
        self.max_price = max_price
        self.bedrooms = bedrooms

    def build_city(self):
        city = f"{self.city.capitalize()}--Spain"
        return city
    
    def build_url(self):
        # Construct the base URL
        base_url = f'https://housinganywhere.com/s/{self.build_city()}'
        
        # Add suffix for the type of apartments based on bedrooms
        if self.bedrooms == '2':
            base_url += '/two-bedroom-apartments'
        elif self.bedrooms == '3':
            base_url += '/three-bedroom-apartments'
        elif self.bedrooms == '1':
            base_url += '/one-bedroom-apartments'
        else:
            base_url += '/apartments'
        
        # Create the parameters list
        params = []

        if self.min_price is not None:
            params.append(f'priceMin={self.min_price}00')
        
        if self.max_price is not None:
            params.append(f'priceMax={self.max_price}00')

        # Append bedroom count as a parameter
        if self.bedrooms:
            params.append(f'bedroomCount={self.bedrooms}')

        # Join the parameters with '&' and add to the URL
        query_string = '&'.join(params)
        full_url = f'{base_url}?{query_string}'
        
        return full_url

    def scrape_listing_details(self, driver, url):
        driver.get(url)
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-md-8.css-1wlzjv3')))

            ### deze functie lukt alleen om titel en size te krijgen ###


            title = driver.find_element(By.CSS_SELECTOR, 'span[data-test-locator="Listing/ListingInfo/street"]').text

            price = ' '

            #price_parent = driver.find_element(By.CSS_SELECTOR, 'div.css-cxuszf-container')
            #price = price_parent.find_element(By.CSS_SELECTOR, 'div > div')
            #for each in price:
                #price = each.text

            size_text = driver.find_element(By.CSS_SELECTOR, 'div.MuiChip-root[data-test-locator="HighlightsTags/Property"]').text
            size = size_text.split(': ')[1]  # Get the size part

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
