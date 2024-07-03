import argparse
from search import Search
from save_data import DatabaseHandler

def main():
    parser = argparse.ArgumentParser(description="Search for apartments and save results to a database.")
    
    parser.add_argument("--city", type=str, required=True, help="City to search in.")
    parser.add_argument("--move_in", type=str, required=True, help="Move-in date (YYYY-MM-DD).")
    parser.add_argument("--move_out", type=str, required=True, help="Move-out date (YYYY-MM-DD).")
    parser.add_argument("--min_price", type=str, required=True, help="Minimum price.")
    parser.add_argument("--max_price", type=str, required=True, help="Maximum price.")
    parser.add_argument("--property_type", type=str, required=True, help="Property type.")
    parser.add_argument("--bedrooms", type=str, required=True, help="Number of bedrooms.")
    
    args = parser.parse_args()
    
    search = Search(
        city=args.city,
        move_in=args.move_in,
        move_out=args.move_out,
        min_price=args.min_price,
        max_price=args.max_price,
        property_type=args.property_type,
        bedrooms=args.bedrooms
    )
    search.execute()
    
    db_handler = DatabaseHandler('listings_db')
    db_handler.create_table()
    
    for result in search.results:
        platform, title, price, size, link = result
        db_handler.insert_listing(platform, title, price, size, link)
        print(result)
    
    db_handler.close()

if __name__ == "__main__":
    main()