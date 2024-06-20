from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class Spotahome:
    def __init__(self, city, move_in, move_out, budget, property_type, bedrooms):
        self.city = city
        self.move_in = move_in
        self.move_out = move_out
        self.budget = budget
        self.property_type = property_type
        self.bedrooms = bedrooms

    def build_url(self):
        base_url = f'https://www.spotahome.com/s/{self.city}'
        params = {}

        if self.move_in and self.move_out:
            params['move-in'] = self.move_in
            params['move-out'] = self.move_out
            move_in_from = (datetime.strptime(self.move_in, '%Y-%m-%d') - timedelta(days=21)).strftime('%Y-%m-%d')
            move_in_to = (datetime.strptime(self.move_out, '%Y-%m-%d') - timedelta(days=14)).strftime('%Y-%m-%d')
            params['moveInFrom'] = move_in_from
            params['moveInTo'] = move_in_to

        if self.budget:
            params['budget'] = self.budget

        property_type_mapping = {
            'apartments': 'apartments',
            'studios': 'studios',
            'rooms': 'rooms-in-shared-apartment',
            'student_residences': 'student-residences'
        }

        if self.property_type in property_type_mapping:
            base_url += f'/for-rent:{property_type_mapping[self.property_type]}'

        if self.bedrooms:
            if self.bedrooms == '3+':
                base_url += '/bedrooms:2/bedrooms:3more'
            else:
                base_url += f'/bedrooms:{self.bedrooms}'

        query_string = '&'.join([f'{key}={value}' for key, value in params.items()])
        full_url = f'{base_url}?{query_string}'
        return full_url

    def scrape_listing_details(self, driver, url):
        driver.get(url)
        try:
            # Wait until the page is fully loaded
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

            # Extract data
            title = driver.find_element(By.CSS_SELECTOR, 'h1.Heading_root__f6nY6.Heading_dark__ehsy6.Heading_large__7KWTX.Heading_left__PpLFb.Heading_inline__UtPZE.property-title__heading').text
            
            prop_type = driver.find_element(By.CSS_SELECTOR, 'div.property-title__details').text.split('\n')[0]
            # Extract general property details and handle size
            general_prop_details = driver.find_element(By.CSS_SELECTOR, 'div.property-title__details').text.split('\n')
            if general_prop_details[-1] == 'm2':
                size = f"{general_prop_details[-2]} {general_prop_details[-1]}"
            else:
                size = None

            # Extract monthly price
            
            price_monthly = driver.find_element(By.CSS_SELECTOR, 'p.listing-pricing-structured__rent').text
            
            # Extract bill details
            bills_section = driver.find_element(By.CSS_SELECTOR, 'div.listing-pricing-structured__bills')
            bills_items = bills_section.find_elements(By.CSS_SELECTOR, 'div.listing-bills-item')
            bills = {}
            for item in bills_items:
                bill_title = item.find_element(By.CSS_SELECTOR, 'div.listing-bills-item__title').text
                bill_value = item.find_element(By.CSS_SELECTOR, 'div.listing-bills-item__value').text
                bills[bill_title] = bill_value
            
            deposit = driver.find_element(By.CSS_SELECTOR, 'p.listing-pricing-structured__security-deposit').text

            return (title, prop_type, size, price_monthly, bills, deposit, url)
        
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
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'l-list__item')))

            # Extract listing URLs
            listings = driver.find_elements(By.CLASS_NAME, 'l-list__item')
            urls = []
            for listing in listings[:5]:  # Limit to the first 10 listings
                link_tag = listing.find_element(By.TAG_NAME, 'a')
                link_url = f"{link_tag.get_attribute('href')}"
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
