from . import CONN, CURSOR
import sqlite3

class Scout:
    def __init__(self, id=None, name=None, region=None):
        self.id = id
        self.name = name
        self.region = region

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
    def region(self):
        return self._region

    @region.setter
    def region(self, value):
        allowed_regions = ['Northeast', 'Southeast', 'Midwest', 'Southwest', 'West', 'East', 'South', 'Northwest', 'North']
        if value is None or (isinstance(value, str) and value.capitalize() in allowed_regions):
            self._region = value
        else:
            raise ValueError(f"Region must be one of {', '.join(allowed_regions)} or None")

    @classmethod
    def create_table(cls):
        """Create the scouts table if it doesn't exist"""
        sql = """
            CREATE TABLE IF NOT EXISTS scouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                region TEXT
            )
        """
        try:
            CURSOR.execute(sql)
            CONN.commit()
        except sqlite3.Error as e:
            print(f"Error creating scouts table: {e}")
            
    @classmethod
    def create(cls, name, region=None):
        """Create a new scout"""
        scout = cls(name=name, region=region)
        scout.save()
        return scout
        
    def save(self):
        """Insert or update the scout in the database"""
        if self.id is None:
            sql = "INSERT INTO scouts (name, region) VALUES (?, ?)"
            params = (self.name, self.region)
        else:
            sql = "UPDATE scouts SET name=?, region=? WHERE id=?"
            params = (self.name, self.region, self.id)
            
        try:
            CURSOR.execute(sql, params)
            if self.id is None:
                self.id = CURSOR.lastrowid
            CONN.commit()
        except sqlite3.Error as e:
            print(f"Error saving scout: {e}")
            CONN.rollback()
            
    @classmethod        
    def get_by_id(cls, scout_id):
        """Retrieve a scout by ID"""
        sql = "SELECT * FROM scouts WHERE id = ?"
        try:
            result = CURSOR.execute(sql, (scout_id,)).fetchone()
            if result:
                return cls(*result)
            return None
        except sqlite3.Error as e:
            print(f"Error retrieving scout by ID {scout_id}: {e}")
            
    @classmethod
    def get_all(cls):
        """Retrieve all scouts"""
        sql = "SELECT * FROM scouts"
        try:
            results = CURSOR.execute(sql).fetchall()
            return [cls(row[0], row[1], row[2]) for row in results]
        except sqlite3.Error as e:
            print(f"Error retrieving scouts: {e}")
            return []
          
    def get_evaluations(self):
        """Retrieve all evaluations made by this scout"""
        sql = "SELECT * FROM evaluations WHERE scout_id = ?"
        try:
            results = CURSOR.execute(sql, (self.id,)).fetchall()
            return results
        except sqlite3.Error as e:
            print(f"Error retrieving evaluations for scout {self.id}: {e}")
            return []