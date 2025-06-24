from conn import connect_to_db
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

class NewUser(BaseModel):
    first_name : str
    last_name : str

class Prediction(BaseModel):
    user_id : int 
    prediction : str
    friend_name : str = None
    friend_prediction : str = None
    stake : int = None

app = FastAPI()

@app.get('/users/{user_id}/predictions')
def get_predictions(user_id: int):
    query = """SELECT * FROM user_prediction
            WHERE user_id =:user_id;"""
    conn = connect_to_db()
    vals = conn.run(query, user_id= user_id)
    cols = [col['name'] for col in conn.columns]
    formatted = [{col: val for col, val in zip(cols, item)} for item in vals]
    return formatted

@app.post('/users')
def create_user(new_user: NewUser):
    query = """INSERT INTO user_info
            (first_name, last_name)
            VALUES
            (:first_name, :last_name);"""
    conn = connect_to_db()
    result = conn.run(query, first_name= new_user.first_name, last_name = new_user.last_name)
    conn.close()
    print(result)
    
@app.get('/users/{user_id}')
def get_user(user_id: int):
    query = """SELECT * FROM user_info 
    WHERE user_id = :user_id;
    """
    conn = connect_to_db()
    vals = conn.run(query, user_id=user_id)
    cols = [col['name'] for col in conn.columns]
    conn.close()
    formatted = [{col: val for col, val in zip(cols, item)} for item in vals]
    return formatted[0]

@app.post('/users/predictions')
def write_predictions(new_prediction: Prediction):
    query = """INSERT INTO user_prediction
            (user_id, prediction, stake, created_at, friend_name, friend_prediction)
            VALUES
            (:user_id, :prediction, :stake, :created_at, :friend_name, :friend_prediction);"""
    conn = connect_to_db()
    created_at = datetime.now().isoformat(timespec="minutes")
    result = conn.run(query, user_id=new_prediction.user_id, 
                      prediction=new_prediction.prediction, stake=new_prediction.stake,
                      created_at= created_at, friend_name=new_prediction.friend_name, 
                      friend_prediction=new_prediction.friend_prediction)
    conn.close()
    print(result)


if __name__ == '__main__':
    new_user = NewUser(first_name="Carlos", last_name="Byrne")
    create_user(new_user)
    # get_predictions()
    new_prediction = Prediction(user_id=1, prediction="Alcaraz to be #1 by EOY")
    write_predictions(new_prediction)
    
