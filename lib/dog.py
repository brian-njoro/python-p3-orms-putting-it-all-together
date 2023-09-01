import sqlite3

CONN = sqlite3.connect('dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    def __init__(self,name,breed):
        self.name = name
        self.breed = breed
        self.id = None

    @classmethod
    def create_table(cls):
        # Create the dogs table if it doesn't exist
        CURSOR.execute('''CREATE TABLE IF NOT EXISTS dogs (
                           id INTEGER PRIMARY KEY,
                           name TEXT,
                           breed TEXT
                        )''')
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute('''DROP TABLE IF EXISTS''')
        CONN.commit()

    def save(self):
        sql = '''INSERT INTO dogs (name,breed) VALUES (?,?)'''
        CURSOR.execute(sql, (self.name, self.breed))

    @classmethod
    def create(cls, name, album):
        dog = Dog(name, album)
        dog.save()
        return dog
    

    @classmethod
    def new_from_db(cls, data_records):
        id, name, breed = data_records
        dog = cls(name, breed)
        dog.id = id
        return dog

    @classmethod
    def get_all(cls):
        CURSOR.execute('''SELECT * FROM dogs''')
        rows = CURSOR.fetchall()
        return [cls.new_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        CURSOR.execute("SELECT * FROM dogs WHERE id = ?", (id,))
        row = CURSOR.fetchone()
        
        return cls.new_from_db(row)
       