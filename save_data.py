import sqlite3

class DatabaseHandler:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS listings (
                    platform TEXT,
                    title TEXT,
                    price TEXT,
                    size TEXT,
                    link TEXT UNIQUE
                )
            """)

    def insert_listing(self, platform, title, price, size, link):
        with self.conn:
            self.conn.execute("""
                INSERT OR IGNORE INTO listings (platform, title, price, size, link)
                VALUES (?, ?, ?, ?, ?)
            """, (platform, title, price, size, link))

    def fetch_all_listings(self):
        with self.conn:
            cursor = self.conn.execute("SELECT * FROM listings")
            return cursor.fetchall()

    def listing_exists(self, link):
        with self.conn:
            cursor = self.conn.execute("SELECT 1 FROM listings WHERE link = ?", (link,))
            return cursor.fetchone() is not None

    def close(self):
        self.conn.close()

