
import psycopg2
from psycopg2 import sql

DB_SETTINGS = {
    "dbname": "photon",
    "user": "student",
    "password": "student",
    "host": "localhost",
    "port": "5432"
}

class PlayerDatabase:
    def __init__(self, use_mock=False):
        self.mock_mode = use_mock
        self.conn = None
        self.cur = None
        self._mock_data = {} if use_mock else None

    def connect(self):
        if self.mock_mode:
            print("[Mock Mode] Skipping DB connection.")
            return
        try:
            self.conn = psycopg2.connect(**DB_SETTINGS)
            self.cur = self.conn.cursor()
            print("[DB] Connected successfully.")
        except Exception as err:
            print(f"[DB] Connection error: {err}")

    def initialize(self):
        if self.mock_mode:
            print("[Mock Mode] Mock DB initialized.")
            return
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INT PRIMARY KEY,
                codename VARCHAR(30) UNIQUE
            );
        """)
        self.conn.commit()

    def add_player(self, player_id, codename):
        if self.mock_mode:
            self._mock_data[player_id] = codename
            print(f"[Mock Mode] Player added: {player_id}, {codename}")
            return
        try:
            self.cur.execute(
                "INSERT INTO players (id, codename) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING;",
                (player_id, codename)
            )
            self.conn.commit()
        except Exception as err:
            print(f"[DB] Error adding player: {err}")

    def get_all(self):
        if self.mock_mode:
            return list(self._mock_data.items())
        try:
            self.cur.execute("SELECT * FROM players;")
            return self.cur.fetchall()
        except Exception as err:
            print(f"[DB] Retrieval error: {err}")
            return []

    def get_by_id(self, player_id):
        if self.mock_mode:
            return (player_id, self._mock_data.get(player_id, "Unknown"))
        try:
            self.cur.execute("SELECT * FROM players WHERE id = %s;", (player_id,))
            return self.cur.fetchone()
        except Exception as err:
            print(f"[DB] Error fetching player: {err}")
            return None

    def close(self):
        if self.mock_mode:
            print("[Mock Mode] No DB to close.")
            return
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        print("[DB] Connection closed.")
