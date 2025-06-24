from pg8000.native import Connection
from dotenv import load_dotenv
import os


load_dotenv(override=True)

def connect_to_db():
    #print(os.getenv("PG_DATABASE"), os.getenv("PG_PORT"))
    return Connection(
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        database=os.getenv("PG_DATABASE"),
        host=os.getenv("PG_HOST"),
        port=os.getenv("PG_PORT"))
    



