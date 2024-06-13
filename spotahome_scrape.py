import requests
from bs4 import BeautifulSoup

class Spotahome:
    def __init__(self, city, availability, budget, property_type):
        self.city = city
        self.availability = availability
        self.budget = budget
        self.property_type = property_type
        self.base_url = self.build_url()
    
    # function to build the url, arguments given in the init function (by the customer). In other words, what houses do you want to scrape?
    def build_url(self):
        base_url = f'https://www.spotahome.com/s/{self.city}'
        
        # Add property type to URL if that argument is given
        if self.property_type:
            base_url += f'/for-rent:{self.property_type}'
        
        # Initialize query parameters
        params = {}
        
        # Add availability dates to query parameters if those arguments are given
        if self.availability:
            params['move-in'] = self.availability
            params['moveInFrom'] = self.availability
            params['moveInTo'] = self.availability
        
        # Add budget range to query parameters if that argument is given
        if self.budget:
            params['budget'] = self.budget
        
        # query string build up
        query_string = '&'.join([f'{key}={value}' for key, value in params.items()])
        
        # Combine base URL with query string 
        # return the 
        full_url = f'{base_url}?{query_string}' if query_string else base_url
        
        return full_url
    
    # function to get all the url's of the listings of the page, based on the build_url function above
    def scrape_listing_urls(self):
        response = requests.get(self.base_url)
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
            
            # Get the URLs of the first 30 listings
            listings = soup.find_all('div', class_='HomecardContent_homecard-content__w-eHe', limit=30)
            urls = []
            for listing in listings:
                link_tag = listing.find('a', class_='HomecardContent_homecard-content__header__4FMs+')
                link_url = f"https://www.spotahome.com{link_tag['href']}" if link_tag else None
                if link_url:
                    urls.append(link_url)
            
            return urls, total_listings
        else:
            print(f"Failed to retrieve content: {response.status_code}")
            return [], 'N/A'
    
    # function to get all the details per listing
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
            return ('N/A', 'N/A', 'N/A', 'N/A', url)
    
    # function to call the scraper and put it in a list
    def scrape(self):
        urls, total_listings = self.scrape_listing_urls()
        
        data = []
        for url in urls:
            listing_details = self.scrape_listing_details(url)
            data.append(listing_details + (total_listings,))
        
        return data

# call the class
spotahome = Spotahome(
    city='barcelona--spain',
    availability='2024-06-14',
    budget='1500-1750',
    property_type='apartments'
)
data = spotahome.scrape()
for each in data:
    print(each)