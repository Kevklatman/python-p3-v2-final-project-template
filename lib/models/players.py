from __init__ import CONN, CURSOR
from evaluations import Evaluation
import sqlite3

class Player:
    def __init__(self, id=None, name=None, position=None, age=None, team=None):
        self._id = id
        self._name = name
        self._position = position
        self._age = age
        self._team = team
        self._evaluations = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name) > 0:
            self._name = name
        else:
            raise ValueError("Name must be a non-empty string")

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        if isinstance(age, int) and age >= 0:
            self._age = age
        else:
            raise ValueError("Age must be a non-negative integer")

    @property
    def team(self):
        return self._team

    @team.setter
    def team(self, team):
        if isinstance(team, int) or isinstance(team, str):
            self._team = team
        else:
            raise ValueError("Team must be an integer or a string")

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        if isinstance(position, str) and len(position) > 0:
            self._position = position
        else:
            raise ValueError("Position must be a non-empty string")

    @classmethod
    def create(cls, name, position, age, team):
        player = cls(name=name, position=position, age=age, team=team)
        player.save()
        return player

    def save(self):
        """Save the player to the database"""
        try:
            CURSOR.execute("""
                INSERT OR REPLACE INTO players (id, name, position, age, team)
                VALUES (?, ?, ?, ?, ?)
            """, (self.id, self.name, self.position, self.age, self.team))
            self._id = CURSOR.lastrowid
            CONN.commit()
        except Exception as e:
            print(f"An error occurred while saving the player: {e}")

    @classmethod
    def get_by_id(cls, player_id):
        """Retrieve a player by ID"""
        try:
            result = CURSOR.execute(
                "SELECT * FROM players WHERE id = ?", (player_id,)
            ).fetchone()
            if result:
                return cls(*result)
            else:
                return None
        except Exception as e:
            print(f"Error retrieving player by ID {player_id}: {e}")
            return None

    @classmethod
    def get_all(cls):
        """Retrieve all players"""
        try:
            results = CURSOR.execute("SELECT * FROM players").fetchall()
            return [cls(*row) for row in results]
        except Exception as e:
            print(f"Error retrieving all players: {e}")
            return []

    @property
    def evaluations(self):
        """Return all evaluations associated with this player"""
        return Evaluation.get_by_player_id(self.id)

    def add_evaluation(self, evaluation):
        """Add an evaluation to this player"""
        if isinstance(evaluation, Evaluation):
            self._evaluations.append(evaluation)
            evaluation.save()
        else:
            raise ValueError("Can only add Evaluation objects")