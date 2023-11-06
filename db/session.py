import mysql.connector
from contextlib import contextmanager 
@contextmanager 
def get_db_connection():
    db = mysql.connector.connect( 
        host="localhost", 
        user="andben", 
        password="Bisidore232425b!", 
        database="db_jobboard" 
    )
    try: 
        yield db 
    finally: 
        db.close() 