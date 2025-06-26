from pg8000.native import Connection
from dotenv import load_dotenv
import os



def connect_to_db():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if os.environ.get("TESTING") != 'True':
        load_dotenv(override=True)
    else:
        path = script_dir + "/tests/testing.env"
        load_dotenv(dotenv_path=path, override=True)


    return Connection(
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        database=os.getenv("PG_DATABASE"),
        host=os.getenv("PG_HOST"),
        port=os.getenv("PG_PORT"))
    



