#!/usr/bin/env python3
# lib/debug.py

from models.__init__ import CONN, CURSOR
import ipdb

def create_table(cls):
        """Create the players table if it doesn't exist"""
        sql = """
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                position TEXT NOT NULL,
                age INTEGER,
                team TEXT
            )
        """
        try:
            CURSOR.execute(sql)
            CONN.commit()
        except sqlite3.Error as e:
            print(f"Error creating players table: {e}")

ipdb.set_trace()
