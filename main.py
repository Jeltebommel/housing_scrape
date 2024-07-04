import argparse
from search import Search
from save_data import DatabaseHandler
import requests

def send_telegram_notification(chat_id, bot_token, new_listings):
    message = "New listings have been found:\n\n"
    for listing in new_listings:
        message += f"Title: {listing[0]}\nPrice: {listing[1]}\nSize: {listing[2]}\nLink: {listing[3]}\n\n"
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print(f"Notification sent to Telegram chat ID {chat_id}")
    else:
        print(f"Failed to send Telegram notification: {response.status_code}, {response.text}")

def main():
    parser = argparse.ArgumentParser(description="Search for apartments and save results to a database.")
    
    parser.add_argument("--city", type=str, required=True, help="City to search in.")
    parser.add_argument("--move_in", type=str, required=True, help="Move-in date (YYYY-MM-DD).")
    parser.add_argument("--move_out", type=str, required=True, help="Move-out date (YYYY-MM-DD).")
    parser.add_argument("--min_price", type=str, required=True, help="Minimum price.")
    parser.add_argument("--max_price", type=str, required=True, help="Maximum price.")
    parser.add_argument("--property_type", type=str, required=True, help="Property type.")
    parser.add_argument("--bedrooms", type=str, required=True, help="Number of bedrooms.")
    parser.add_argument("--telegram_chat_id", type=str, required=True, help="Telegram chat ID to send notifications.")
    parser.add_argument("--telegram_bot_token", type=str, required=True, help="Telegram bot token to send notifications.")
    
    args = parser.parse_args()
    
    search = Search(
        city=args.city,
        move_in=args.move_in,
        move_out=None if args.move_out == "None" else args.move_out,
        min_price=args.min_price,
        max_price=args.max_price,
        property_type=args.property_type,
        bedrooms=None if args.bedrooms == "None" else args.bedrooms
    )
    
    if search.property_type == 'room':
        search.execute_room()
    elif search.property_type == 'studio':
        search.execute_studio()
    elif search.property_type == 'apartment':
        search.execute_apartment()
    
    db_handler = DatabaseHandler('listing_db')

    # Fetch existing listings
    existing_listings = db_handler.fetch_all_listings()
    existing_links = [listing[5] for listing in existing_listings]

    new_listings = []

    for result in search.results:
        title, price, size, link = result
        platform = "Spotahome" if "spotahome" in link else "ThinkSpain" if "thinkspain" in link else "Ukio" if "ukio" in link else "Properstar" if "properstar" in link else "RealEstate" if "realestate" in link else "Unknown"
        
        if link not in existing_links:
            db_handler.insert_listing(platform, title, price, size, link)
            new_listings.append(result)
            print(f"New listing found: {result}")
    
    if not new_listings:
        print("No new listings found.")
    else:
        send_telegram_notification(args.telegram_chat_id, args.telegram_bot_token, new_listings)
    
    db_handler.close()

if __name__ == "__main__":
    main()
