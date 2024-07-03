from platforms.spotahome import Spotahome
from platforms.properstar import Properstar
from platforms.housing_anywhere import HousingAnywhere
from platforms.thinkspain import ThinkSpain
from platforms.ukio import Ukio
from platforms.real_estate import RealEstate

class Search:
    def __init__(self, city, move_in=None, move_out=None, min_price=None, max_price=None, property_type=None, bedrooms=None):
        self.city = city
        self.move_in = move_in
        self.move_out = move_out
        self.min_price = min_price
        self.max_price = max_price
        self.property_type = property_type
        self.bedrooms = bedrooms
        self.platforms_room = [
            #HousingAnywhere(city, min_price, max_price, property_type, bedrooms),
            Spotahome(city, move_in, move_out, min_price, max_price, property_type, bedrooms),
            Properstar(city, min_price, max_price, property_type, bedrooms),
        ]
        self.platforms_studio = [
            #HousingAnywhere(city, min_price, max_price, property_type, bedrooms),
            Spotahome(city, move_in, move_out, min_price, max_price, property_type, bedrooms),
        ]
        self.platforms_apartment = [
            #HousingAnywhere(city, min_price, max_price, property_type, bedrooms),
            Spotahome(city, move_in, move_out, min_price, max_price, property_type, bedrooms),
            Properstar(city, min_price, max_price, property_type, bedrooms),
            ThinkSpain(city, min_price, max_price, bedrooms),
            Ukio(city, check_in=move_in, check_out=move_out, bedrooms=bedrooms, rent_from=min_price, rent_to=max_price),
            RealEstate(city, min_price, max_price, bedrooms)
        ]
        self.results = []

    def execute_room(self):
        for platform in self.platforms_room:
            listings = platform.scrape()
            for listing in listings:
                self.results.append(listing)
    
    def execute_studio(self):
        for platform in self.platforms_studio:
            listings = platform.scrape()
            for listing in listings:
                self.results.append(listing)
    
    def execute_apartment(self):
        for platform in self.platforms_apartment:
            listings = platform.scrape()
            for listing in listings:
                self.results.append(listing)



