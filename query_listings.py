import sqlite3

def view_listings():
    conn = sqlite3.connect("listing_db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM listings")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()

print(view_listings())
