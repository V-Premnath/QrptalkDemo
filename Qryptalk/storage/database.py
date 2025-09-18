import sqlite3

class Database:
    """
    Handles SQLite database operations.
    """
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self._initialize_schema()

    def _initialize_schema(self):
        # Create tables if they don't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contact_id TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.connection.commit()

    def execute_query(self, query, params=None):
        if params is None:
            params = []
        self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()
