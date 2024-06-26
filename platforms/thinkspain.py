from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class ThinkSpain:
    def __init__(self, city, bedrooms, min_price, max_price):
        self.city = city
        self.bedrooms = bedrooms
        self.min_price = min_price
        self.max_price = max_price

    def build_url(self):
        base_url = f"https://www.thinkspain.com/property-to-rent-long-term/{self.city}"
        params = []

        if self.min_price:
            params.append(f"minprice={self.min_price}")
        if self.max_price:
            params.append(f"maxprice={self.max_price}")
        if self.bedrooms:
            if self.bedrooms == "exactly_2":
                params.append("beds=e2")
            else:
                params.append(f"beds={self.bedrooms}")

        if params:
            return f"{base_url}?" + "&".join(params)
        else:
            return base_url
        

    def get_listing_urls(self):
        url = self.build_url()
        print(f"Scraping from: {url}")

        driver = webdriver.Chrome()
        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'container')))

            listings = driver.find_elements(By.CSS_SELECTOR, 'div.twc__grid-item.twc__property-grid-item.position-relative')

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

    def get_listing_details(self):
        urls = self.get_listing_urls()

        data = []

        driver = webdriver.Chrome()
        
        try:
            for url in urls:
                driver.get(url)
                
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.pagepopup__content')))

                loop = driver.find_elements(By.CSS_SELECTOR, 'div.pagepopup__content')
                for each in loop:
                    title = each.text.split('\n')[10]
                    price = each.text.split('\n')[1]
                    size = each.text.split('\n')[11]
                
                data.append((title, price, size, url))
                
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error while scraping {url}: {e}")
            data.append('N/A')
        finally:
            driver.quit()

        return data


think_spain = ThinkSpain(city="barcelona-city", min_price=700, max_price=2000, bedrooms="2")

output = think_spain.get_listing_details()
print(output)