from platforms.spotahome import Spotahome

class Search:
    def __init__(self, city, move_in=None, move_out=None, budget=None, property_type=None, bedrooms=None):
        self.city = city
        self.move_in = move_in
        self.move_out = move_out
        self.budget = budget
        self.property_type = property_type
        self.platforms = [Spotahome(city, move_in, move_out, budget, property_type, bedrooms)]
        self.results = []

    def execute(self):
        for platform in self.platforms:
            listings = platform.scrape()
            for listing in listings:
                self.results.append(listing)



