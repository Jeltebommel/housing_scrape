from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class Ukio:
    def __init__(self, city, check_in=None, check_out=None, bedrooms=None, exact_bedrooms=False, rent_from=None, rent_to=None):
        self.city = city
        self.check_in = check_in
        self.check_out = check_out
        self.bedrooms = bedrooms
        self.exact_bedrooms = exact_bedrooms
        self.rent_from = rent_from
        self.rent_to = rent_to
    
    def build_city(self):
        return self.city

    def build_url(self):
        base_url = f'https://ukio.com/apartments/{self.build_city()}'
        params = {}

        if self.check_in:
            params['check_in'] = self.check_in
        if self.check_out:
            params['check_out'] = self.check_out
        if self.bedrooms is not None:
            params['bedrooms'] = self.bedrooms
            if self.exact_bedrooms:
                params['exact_bedrooms'] = 'true'
        if self.rent_from:
            params['rent_from'] = self.rent_from
        if self.rent_to:
            params['rent_to'] = self.rent_to

        query_string = urlencode(params)
        full_url = f'{base_url}?{query_string}' if query_string else base_url
        return full_url

    def get_listing_urls(self):
        url = self.build_url()
        print(f"URL: {url}")

        driver = webdriver.Chrome()
        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'flex.flex-col.pt-20')))

            listings = driver.find_elements(By.CSS_SELECTOR, 'li.flex.flex-col.gap-x-6.bg-white')

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
                
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'main')))

                title = driver.find_element(By.CSS_SELECTOR, 'section.space-y-2.bg-white h1').text

                size_elements = driver.find_element(By.CSS_SELECTOR, 'div.font-form.grid.grid-flow-row').text.split('\n')
                size = ' '.join(size_elements) if isinstance(size_elements, list) else size_elements

                price = driver.find_element(By.CSS_SELECTOR, 'div.mt-8.mb-8.flex.w-full.flex-col').text




                ### Title lukt wel, price en size kan ik niet vinden ###

                #price = driver.find_element(By.CSS_SELECTOR, 'span.whitespace-nowrap').text

                # Locate the element for size
                #size = driver.find_elements(By.CSS_SELECTOR, 'div.font-form.grid.grid-flow-row.auto-rows-max.grid-cols-2.gap-x-6.pt-2.text-xs.md:auto-cols-max.md:grid-flow-col.md:grid-cols-none.md:pt-4.md:text-sm').text
                
                
                data.append((title, price, size, url))
                
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error while scraping {url}: {e}")
            data.append('N/A')
        finally:
            driver.quit()

        return data
