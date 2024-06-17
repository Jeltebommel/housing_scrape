from datetime import datetime
import requests
from bs4 import BeautifulSoup

class Spotahome:
    def __init__(self, city, move_in_from=None, move_in_to=None, budget=None, property_type=None):
        self.city = city
        self.move_in_from = move_in_from
        self.move_in_to = move_in_to
        self.budget = budget
        self.property_type = property_type

    def build_url(self):
        base_url = f'https://www.spotahome.com/s/{self.city}'
        params = {}

        if self.move_in_from and self.move_in_to:
            params['moveInFrom'] = self.move_in_from
            params['moveInTo'] = self.move_in_to
            params['move-in'] = self.move_in_from

        if self.budget:
            params['budget'] = self.budget

        if self.property_type:
            base_url += f'/for-rent:{self.property_type}'

        query_string = '&'.join([f'{key}={value}' for key, value in params.items()])
        full_url = f'{base_url}?{query_string}'

        return full_url

    def scrape_listing_details(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Title
            title_tag = soup.find('p', class_='HomecardContent_homecard-content__title__rVQuY')
            title_text = title_tag.get_text(strip=True) if title_tag else 'N/A'
            
            # Property type
            prop_type_tag = soup.find('span', class_='HomecardContent_homecard-content__type__tsM0N')
            prop_type_text = prop_type_tag.get_text(strip=True) if prop_type_tag else 'N/A'
            
            # Available date
            available_date_tag = soup.find('span', class_='HomecardContent_homecard-content__available-from__MFrSP')
            available_date_text = available_date_tag.get_text(strip=True) if available_date_tag else 'N/A'
            
            # Price
            price_tag = soup.find('span', class_='Price_price__nTFG1')
            price_text = price_tag.get_text(strip=True) if price_tag else 'N/A'
            
            return (title_text, prop_type_text, available_date_text, price_text, url)
        else:
            print(f"Failed to retrieve content from {url}: {response.status_code}")

    def scrape(self):
        url = self.build_url()
        print("Scraping URL:", url)
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Get the total number of listings
            total_listings_div = soup.find('div', class_='search-listing__total-results')
            if total_listings_div:
                strong_tag = total_listings_div.find('strong')
                total_listings = strong_tag.get_text(strip=True) if strong_tag else 'N/A'
                print("Total Listings:", total_listings)
            else:
                total_listings = 'N/A'
            
            # Get the URLs of the first 10 listings
            listings = soup.find_all('div', class_='HomecardContent_homecard-content__w-eHe', limit=10)
            urls = []
            for listing in listings:
                link_tag = listing.find('a', class_='HomecardContent_homecard-content__header__4FMs+')
                link_url = f"https://www.spotahome.com{link_tag['href']}" if link_tag else None
                if link_url:
                    urls.append(link_url)
            
            # Scrape details for each listing
            data = []
            for url in urls:
                listing_details = self.scrape_listing_details(url)
                data.append(listing_details + (total_listings,))
            
            return data
        else:
            print(f"Failed to retrieve content: {response.status_code}")
            return []

# Example usage
spotahome = Spotahome(
    city='barcelona--spain',
    move_in_from='2024-06-14',
    move_in_to='2024-07-14',
    budget='1500-1750',
    property_type='apartments'
)
data = spotahome.scrape()

# Print the extracted data
for entry in data:
    print(entry)
