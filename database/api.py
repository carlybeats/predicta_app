from conn import connect_to_db
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

class NewUser(BaseModel):
    first_name : str
    last_name : str

class Prediction(BaseModel):
    prediction : str
    friend_name : str = None
    friend_prediction : str = None
    stake : int = None


app = FastAPI()

@app.get('/users/{user_id}/predictions', status_code=200)
def get_predictions(user_id: int):
    query = """SELECT * FROM user_prediction
            WHERE user_id =:user_id;"""
    conn = connect_to_db()
    vals = conn.run(query, user_id= user_id)
    cols = [col['name'] for col in conn.columns]
    formatted = [{col: val for col, val in zip(cols, item)} for item in vals]
    return formatted

@app.post('/users', status_code=201)
def create_user(new_user: NewUser):
    try:
        query = """INSERT INTO user_info
                (first_name, last_name)
                VALUES
                (:first_name, :last_name);"""
        conn = connect_to_db()
        result = conn.run(query, first_name= new_user.first_name, last_name = new_user.last_name)
    except Exception as e:
        print("EXCEPTION", e)
    conn.close()
    return {"success": "new user created"}
    
@app.get('/users/{user_id}', status_code=200)
def get_user(user_id: int):
    query = """SELECT * FROM user_info 
    WHERE user_id = :user_id;
    """
    conn = connect_to_db()
    vals = conn.run(query, user_id=user_id)
    cols = [col['name'] for col in conn.columns]
    conn.close()
    formatted = [{col: val for col, val in zip(cols, item)} for item in vals]
    try:
        return formatted[0]
    except:
        return {"error": "user not found"}

@app.post('/users/{user_id}/predictions', status_code=201)
def write_predictions(new_prediction: Prediction, user_id: int):
    query = """INSERT INTO user_prediction
            (user_id, prediction, stake, created_at, friend_name, friend_prediction)
            VALUES
            (:user_id, :prediction, :stake, :created_at, :friend_name, :friend_prediction);"""
    conn = connect_to_db()
    created_at = datetime.now().isoformat(timespec="minutes")
    result = conn.run(query, user_id=user_id, 
                      prediction=new_prediction.prediction, stake=new_prediction.stake,
                      created_at= created_at, friend_name=new_prediction.friend_name, 
                      friend_prediction=new_prediction.friend_prediction)
    conn.close()
    return {"success": "prediction made"}

# need to implement proper HTTP response codes
    
