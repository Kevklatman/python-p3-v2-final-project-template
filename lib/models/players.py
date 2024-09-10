from . import CONN, CURSOR
import sqlite3

class Player:
    def __init__(self, id=None, name=None, position=None, age=None, team=None):
        self.id = id
        self.name = name
        self.position = position
        self.age = age
        self.team = team

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if value is None or isinstance(value, int):
            self._id = value
        else:
            raise ValueError("ID must be an integer or None")
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value and isinstance(value, str):
            self._name = value.strip()
        else:
            raise ValueError("Name must be a non-empty string")

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if value is None or (isinstance(value, int) and value >= 0):
            self._age = value
        else:
            raise ValueError("Age must be a non-negative integer or None")

    @property
    def team(self):
        return self._team

    @team.setter
    def team(self, value):
        if value is None or isinstance(value, str):
            self._team = value
        else:
            raise ValueError("Team must be a string or None")

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        allowed_positions = ['P', 'C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'DH']
        if value in allowed_positions:
            self._position = value
        else:
            raise ValueError(f"Invalid position. Must be one of: {', '.join(allowed_positions)}")

    @classmethod
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

    @classmethod
    def create(cls, name, position, age=None, team=None):
        """Create a new player"""
        player = cls(name=name, position=position, age=age, team=team)
        player.save()
        return player

    def save(self):
        """Insert or update the player in the database"""
        if self.id is None:
            sql = "INSERT INTO players (name, position, age, team) VALUES (?, ?, ?, ?)"
            params = (self.name, self.position, self.age, self.team)
        else:
            sql = "UPDATE players SET name=?, position=?, age=?, team=? WHERE id=?"
            params = (self.name, self.position, self.age, self.team, self.id)

        try:
            CURSOR.execute(sql, params)
            if self.id is None:
                self.id = CURSOR.lastrowid
            CONN.commit()
        except sqlite3.Error as e:
            print(f"Error saving player: {e}")
            CONN.rollback()

    @classmethod
    def get_by_id(cls, player_id):
        """Retrieve a player by ID"""
        sql = "SELECT * FROM players WHERE id = ?"
        try:
            result = CURSOR.execute(sql, (player_id,)).fetchone()
            if result:
                return cls(*result)
            return None
        except sqlite3.Error as e:
            print(f"Error retrieving player by ID {player_id}: {e}")

    @classmethod
    def get_all(cls):
        """Retrieve all players"""
        sql = "SELECT * FROM players"
        try:
            results = CURSOR.execute(sql).fetchall()
            return [cls(*row) for row in results]
        except sqlite3.Error as e:
            print(f"Error retrieving players: {e}")
            return []

    def get_evaluations(self):
        """Retrieve all evaluations for this player"""
        sql = "SELECT * FROM evaluations WHERE player_id = ?"
        try:
            results = CURSOR.execute(sql, (self.id,)).fetchall()
            return results
        except sqlite3.Error as e:
            print(f"Error retrieving evaluations for player {self.id}: {e}")
            return []