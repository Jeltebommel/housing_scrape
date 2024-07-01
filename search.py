from platforms.spotahome import Spotahome
from platforms.properstar import Properstar
from platforms.housing_anywhere import HousingAnywhere
from platforms.thinkspain import ThinkSpain
from platforms.ukio import Ukio
from platforms.real_estate import RealEstate

class Search:
    def __init__(self, city, move_in=None, move_out=None, min_price=None, max_price=None, bedrooms=None):
        self.city = city
        self.move_in = move_in
        self.move_out = move_out
        self.min_price = min_price
        self.max_price = max_price
        self.bedrooms = bedrooms
        self.platforms = [
            HousingAnywhere(city, min_price, max_price, bedrooms),
            Spotahome(city, move_in, move_out, min_price, max_price, bedrooms),
            Properstar(city, min_price, max_price, bedrooms),
            ThinkSpain(city, min_price, max_price, bedrooms),
            Ukio(city, check_in=move_in, check_out=move_out, bedrooms=bedrooms, rent_from=min_price, rent_to=max_price),
            RealEstate(city, min_price, max_price, bedrooms)
        ]
        self.results = []

    def execute(self):
        for platform in self.platforms:
            listings = platform.scrape()
            for listing in listings:
                self.results.append(listing)

