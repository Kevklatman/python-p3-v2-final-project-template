from __init__ import CONN, CURSOR
from scout import Scout
from players import Player

class Evaluation:
    def __init__(self, id=None, scout_id=None, player_id=None, date=None, grade=None, notes=None, player_comparison=None):
        self._id = id
        self._scout_id = scout_id
        self._player_id = player_id
        self._date = date
        self._grade = grade
        self._notes = notes
        self._player_comparison = player_comparison

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        if isinstance(id, int) and id > 0:
            self._id = id
        else:
            raise ValueError("ID must be a positive integer.")

    @property
    def scout(self):
        return self._scout

    @scout.setter
    def scout(self, scout):
        if isinstance(scout, Scout):
            self._scout = scout
        else:
            raise ValueError("Scout must be an instance of the Scout class.")

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, player):
        if isinstance(player, Player):
            self._player = player
        else:
            raise ValueError("Player must be an instance of the Player class.")

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        if isinstance(date, str) and date.strip() != "":
            self._date = date
        else:
            raise ValueError("Date must be a non-empty string.")

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, grade):
        if isinstance(grade, str) and len(grade) == 1 and grade.upper() in ['A', 'B', 'C', 'D', 'F']:
            self._grade = grade.upper()
        else:
            raise ValueError("Grade must be a single uppercase letter (A, B, C, D, F).")

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, notes):
        if isinstance(notes, str):
            self._notes = notes
        else:
            raise ValueError("Notes must be a string.")
    
    @classmethod
    def create_table(cls):
        """Create a new table to persist the attributes of Evaluations instances"""
        sql = """
            CREATE TABLE IF NOT EXISTS evaluations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scout_id INTEGER,
            player_id INTEGER,
            date DATE,
            grade TEXT,
            notes TEXT,
            player_comparison TEXT
            )
        """
        try:
            CURSOR.execute(sql)
            CONN.commit()
        except Exception as e:
            print(f"An error occurred while creating the table: {e}")

    def save(self):
        """Save the evaluation to the database"""
        try:
            CURSOR.execute("""
                INSERT OR REPLACE INTO evaluations (id, scout_id, player_id, date, grade, notes, player_comparison)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (self.id, self.scout_id, self.player_id, self.date, self.grade, self.notes, self.player_comparison))
            self._id = CURSOR.lastrowid
            CONN.commit()
        except Exception as e:
            print(f"An error occurred while saving the evaluation: {e}")

    @classmethod
    def get_by_scout_id(cls, scout_id):
        """Retrieve all evaluations for a given scout_id"""
        try:
            result = CURSOR.execute(
                "SELECT * FROM evaluations WHERE scout_id = ?", (scout_id,)
            ).fetchall()
            return [cls(*row) for row in result] or []
        except Exception as e:
            print(f"Error retrieving evaluations for scout_id {scout_id}: {e}")
            return []

    @classmethod
    def get_by_player_id(cls, player_id):
        """Retrieve all evaluations for a given player_id"""
        try:
            result = CURSOR.execute(
                "SELECT * FROM evaluations WHERE player_id = ?", (player_id,)
            ).fetchall()
            return [cls(*row) for row in result] or []
        except Exception as e:
            print(f"Error retrieving evaluations for player_id {player_id}: {e}")
            return []
        
    @classmethod
    def create(cls, scout_id, player_id, date, grade, notes, player_comparison=None):
        evaluation = cls(scout_id=scout_id, player_id=player_id, date=date, grade=grade, notes=notes, player_comparison=player_comparison)
        evaluation.save()
        return evaluation