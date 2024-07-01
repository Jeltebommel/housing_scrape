import sqlite3

class DatabaseHandler:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            title TEXT,
            price TEXT,
            size TEXT,
            link TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def insert_listing(self, platform, title, price, size, link):
        query = """
        INSERT INTO listings (platform, title, price, size, link)
        VALUES (?, ?, ?, ?, ?)
        """
        self.conn.execute(query, (platform, title, price, size, link))
        self.conn.commit()

    def close(self):
        self.conn.close()
