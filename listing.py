class Listing:
    def __init__(self, title, price, location, start_date, end_date=None, platform=None, square_meters=None):
        self.title = title
        self.price = price
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.platform = platform
        self.square_meters = square_meters

    def __str__(self):
        return f"{self.title} - {self.price} - {self.location}"

