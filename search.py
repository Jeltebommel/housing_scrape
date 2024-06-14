from platforms.spotahome import Spotahome

class Search:
    def __init__(self, city, availability, budget, property_type):
        self.city = city
        self.availability = availability
        self.budget = budget
        self.property_type = property_type
        self.platforms = [Spotahome(city, availability, budget, property_type)]
        self.results = []

    def execute(self):
        for platform in self.platforms:
            self.results.append(platform.scrape())
