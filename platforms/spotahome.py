from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class Spotahome:
    def __init__(self, city, move_in, move_out, min_price, max_price, bedrooms):
        self.city = city
        self.move_in = move_in
        self.move_out = move_out
        self.min_price = min_price
        self.max_price = max_price
        self.bedrooms = bedrooms

    def build_city(self):
        city = f"{self.city}--spain"
        return city

    def build_url(self):
        base_url = f'https://www.spotahome.com/s/{self.build_city()}'
        params = {}

        if self.move_in and self.move_out:
            params['move-in'] = self.move_in
            params['move-out'] = self.move_out
            move_in_from = (datetime.strptime(self.move_in, '%Y-%m-%d') - timedelta(days=21)).strftime('%Y-%m-%d')
            move_in_to = (datetime.strptime(self.move_out, '%Y-%m-%d') - timedelta(days=14)).strftime('%Y-%m-%d')
            params['moveInFrom'] = move_in_from
            params['moveInTo'] = move_in_to

        if self.min_price or self.max_price:
            budget = f"{self.min_price}-{self.max_price}"
            params['budget'] = budget

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
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

            title = driver.find_element(By.CSS_SELECTOR, 'h1.Heading_root__f6nY6.Heading_dark__ehsy6.Heading_large__7KWTX.Heading_left__PpLFb.Heading_inline__UtPZE.property-title__heading').text
            general_prop_details = driver.find_element(By.CSS_SELECTOR, 'div.property-title__details').text.split('\n')
            if general_prop_details[-1] == 'm2':
                size = f"{general_prop_details[-2]} {general_prop_details[-1]}"
            else:
                size = None

            price = driver.find_element(By.CSS_SELECTOR, 'p.listing-pricing-structured__rent').text

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
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'l-list__item')))

            listings = driver.find_elements(By.CLASS_NAME, 'l-list__item')
            urls = []
            for listing in listings[:5]:
                link_tag = listing.find_element(By.TAG_NAME, 'a')
                link_url = f"{link_tag.get_attribute('href')}"
                urls.append(link_url)

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
