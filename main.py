from search import Search
from save_data import DatabaseHandler

if __name__ == "__main__":
    # Initialize the database handler
    db_handler = DatabaseHandler('listing_db')
    
    search = Search(
        city='barcelona',
        move_in='2025-01-01',
        move_out='2025-06-30',
        min_price='500',
        max_price='3000',
        bedrooms='2'
    )
    search.execute()

    # Insert the results into the database
    for result in search.results:
        
        title, price, size, link = result
        platform = "HousingAnywhere" if "housinganywhere" in link else "Spotahome" if "spotahome" in link else "ThinkSpain" if "thinkspain" in link else "Ukio" if "ukio" in link else "Properstar" if "properstar" in link else "RealEstate" if "realestate" in link else "Unknown"

        # Insert listing into the database
        db_handler.insert_listing(platform, title, price, size, link)

    # Close the database connection
    db_handler.close()
