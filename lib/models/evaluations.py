from . import CONN, CURSOR
from datetime import datetime
import sqlite3

class Evaluation:
    def __init__(self, id=None, scout_id=None, player_id=None, date=None, grade=None, notes=None, player_comparison=None):
        self.id = id
        self.scout_id = scout_id
        self.player_id = player_id
        self.date = date
        self.grade = grade
        self.notes = notes
        self.player_comparison = player_comparison

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if value is None or (isinstance(value, int) and value > 0):
            self._id = value
        else:
            raise ValueError("ID must be a positive integer or None.")

    @property
    def scout_id(self):
        return self._scout_id

    @scout_id.setter
    def scout_id(self, value):
        if value is None or (isinstance(value, int) and value > 0):
            self._scout_id = value
        else:
            raise ValueError("Scout ID must be a positive integer or None.")

    @property
    def player_id(self):
        return self._player_id

    @player_id.setter  
    def player_id(self, value):
        if value is None or (isinstance(value, int) and value > 0):
            self._player_id = value
        else:
            raise ValueError("Player ID must be a positive integer or None.")

    @property 
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date= value

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, value):
        allowed_grades = ['A', 'B', 'C', 'D', 'F'] 
        if value is None or (isinstance(value, str) and value.upper() in allowed_grades):
            self._grade = value
        else:
            raise ValueError(f"Grade must be one of {', '.join(allowed_grades)} or None.")

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, value):
        if value is None or isinstance(value, str):
            self._notes = value
        else:
            raise ValueError("Notes must be a string or None.")
        
    @property
    def player_comparison(self):
        return self._player_comparison
        
    @player_comparison.setter  
    def player_comparison(self, value):
        if value is None or isinstance(value, str):
            self._player_comparison = value
        else:
            raise ValueError("Player comparison must be a string or None.")
            
    @classmethod
    def create_table(cls):
        """Create the evaluations table if it doesn't exist"""
        sql = """
            CREATE TABLE IF NOT EXISTS evaluations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scout_id INTEGER,
                player_id INTEGER,
                date TIMESTAMP,
                grade TEXT,
                notes TEXT,
                player_comparison TEXT,
                FOREIGN KEY (scout_id) REFERENCES scouts (id),
                FOREIGN KEY (player_id) REFERENCES players (id)
            )  
        """
        try:
            CURSOR.execute(sql)
            CONN.commit()
        except sqlite3.Error as e:
            print(f"Error creating evaluations table: {e}")

    @classmethod
    def create(cls, scout_id, player_id, date, grade, notes=None, player_comparison=None):
        """Create a new evaluation"""
        evaluation = cls(scout_id=scout_id, player_id=player_id, date=date, grade=grade, notes=notes, player_comparison=player_comparison)
        evaluation.save()
        return evaluation
        
    def save(self):
        """Insert or update the evaluation in the database"""
        if self.id is None:
            sql = "INSERT INTO evaluations (scout_id, player_id, date, grade, notes, player_comparison) VALUES (?, ?, ?, ?, ?, ?)" 
            params = (self.scout_id, self.player_id, self.date, self.grade, self.notes, self.player_comparison)
        else:
            sql = "UPDATE evaluations SET scout_id=?, player_id=?, date=?, grade=?, notes=?, player_comparison=? WHERE id=?"
            params = (self.scout_id, self.player_id, self.date, self.grade, self.notes, self.player_comparison, self.id)
            
        try:
            CURSOR.execute(sql, params)
            if self.id is None:
                self.id = CURSOR.lastrowid
            CONN.commit()
        except sqlite3.Error as e:
            print(f"Error saving evaluation: {e}")
            CONN.rollback()
            
    @classmethod
    def get_by_id(cls, eval_id):
        """Retrieve an evaluation by ID"""
        sql = "SELECT * FROM evaluations WHERE id = ?"
        try:
            result = CURSOR.execute(sql, (eval_id,)).fetchone()
            if result:
                return cls(*result)
            return None  
        except sqlite3.Error as e:
            print(f"Error retrieving evaluation by ID {eval_id}: {e}")
            
    @classmethod
    def get_by_scout_id(cls, scout_id):
        """Retrieve all evaluations for a given scout_id"""
        sql = "SELECT * FROM evaluations WHERE scout_id = ?"
        try:
            results = CURSOR.execute(sql, (scout_id,)).fetchall()
            return [cls(*row) for row in results]
        except sqlite3.Error as e:  
            print(f"Error retrieving evaluations for scout {scout_id}: {e}")
            return []
            
    @classmethod 
    def get_by_player_id(cls, player_id):
        """Retrieve all evaluations for a given player_id"""
        sql = "SELECT * FROM evaluations WHERE player_id = ?"
        try:
            results = CURSOR.execute(sql, (player_id,)).fetchall() 
            return [cls(*row) for row in results]
        except sqlite3.Error as e:
            print(f"Error retrieving evaluations for player {player_id}: {e}")
            return []
        
    @classmethod
    def get_all(cls):
        """Retrieve all evaluations"""
        sql = "SELECT * FROM evaluations"
        try:
            results = CURSOR.execute(sql).fetchall()
            return [cls(*row) for row in results]
        except sqlite3.Error as e:
            print(f"Error retrieving evaluations: {e}")
            return []

    def update(self, scout_id=None, player_id=None, date=None, grade=None, notes=None, player_comparison=None):
        """Update the evaluation with new values"""
        if scout_id is not None:
            self.scout_id = scout_id
        if player_id is not None:
            self.player_id = player_id
        if date is not None:
            self.date = date
        if grade is not None:
            self.grade = grade
        if notes is not None:
            self.notes = notes
        if player_comparison is not None:
            self.player_comparison = player_comparison
        self.save()
