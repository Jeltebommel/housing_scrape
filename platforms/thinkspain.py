from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class ThinkSpain:
    def __init__(self, city, min_price, max_price, bedrooms):
        self.city = city
        self.min_price = min_price
        self.max_price = max_price
        self.bedrooms = bedrooms

    def build_city(self):
        city = f"{self.city}-city"
        return city

    def build_url(self):
        base_url = f"https://www.thinkspain.com/property-to-rent-long-term/{self.build_city()}&order=RecentFirst"
        params = []

        if self.min_price is not None:
            params.append(f"minprice={self.min_price}")
        if self.max_price is not None:
            params.append(f"maxprice={self.max_price}")
        if self.bedrooms is not None:
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
                
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.pagepopup__content')))

                ### check even of jij de juiste css_selector kan vinden voor title size en price ###

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

think_spain = ThinkSpain("barcelona", min_price=500, max_price=3000, bedrooms=2)
url = think_spain.build_url()
print(url)