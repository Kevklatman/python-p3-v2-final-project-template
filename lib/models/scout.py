from __init__ import CONN, CURSOR
from players import Player
from evaluations import Evaluation

class Scout:
    def __init__(self, id=None, name=None, region=None):
        self._id = id
        self._name = name
        self._region = region
        self._evaluations = []  

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name) >= 1:
            self._name = name
        else:
            raise ValueError("Name must be a non-empty string")

    @property
    def region(self):
        return self._region

    @region.setter
    def region(self, region):
        if isinstance(region, str) and len(region) > 0:
            self._region = region
        else:
            raise ValueError("Region must be a non-empty string")

    @classmethod
    def create(cls, name, region):
        """Initialize a new Scout instance and save the object to the database"""
        scout = cls(name, region)
        scout.save()
        return scout

    def save(self):
        """Save the scout to the database"""
        try:
            CURSOR.execute("""
                INSERT OR REPLACE INTO scouts (id, name, region)
                VALUES (?, ?, ?)
            """, (self.id, self.name, self.region))
            self._id = CURSOR.lastrowid
            CONN.commit()
        except Exception as e:
            print(f"An error occurred while saving the scout: {e}")

    @classmethod
    def get_by_id(cls, scout_id):
        """Retrieve a scout by ID"""
        try:
            result = CURSOR.execute(
                "SELECT * FROM scouts WHERE id = ?", (scout_id,)
            ).fetchone()
            if result:
                return cls(*result)
            else:
                return None
        except Exception as e:
            print(f"Error retrieving scout by ID {scout_id}: {e}")
            return None

    @classmethod
    def get_all(cls):
        """Retrieve all scouts"""
        try:
            results = CURSOR.execute("SELECT * FROM scouts").fetchall()
            return [cls(*row) for row in results]
        except Exception as e:
            print(f"Error retrieving all scouts: {e}")
            return []

    @property
    def evaluations(self):
        """Return all evaluations associated with this scout"""
        return Evaluation.get_by_scout_id(self.id)

    def add_evaluation(self, evaluation):
        """Add an evaluation to this scout"""
        if isinstance(evaluation, Evaluation):
            self._evaluations.append(evaluation)
            evaluation.save()
        else:
            raise ValueError("Can only add Evaluation objects")