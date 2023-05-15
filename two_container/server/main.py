import numpy as np
# import tensorflow as tf
# from tensorflow import keras
from numpy import genfromtxt
import joblib
from fastapi import FastAPI
import requests
import json
from pydantic import BaseModel

# load user, item data
user_vecs = genfromtxt('./data/user_vecs.csv', delimiter=',')
item_vecs = genfromtxt('./data/item_vecs.csv', delimiter=',')
item_embeddings = genfromtxt('./data/item_embeddings.csv', delimiter=',')
vms = item_embeddings

# create user feature dict
user_dict = {}
for i in range(len(user_vecs)):
    user_dict[int(user_vecs[i][0])] = user_vecs[i]

# load scaler
scalerUser = joblib.load('scalerUser.save')
scalerItem = joblib.load('scalerItem.save')
scalerTarget = joblib.load('scalerTarget.save')

# load model
# model = tf.keras.models.load_model('user_embedding_model')

# retrieve function

def retrieve(uid):
    #compute user embedding
    user_vec = user_dict[uid].reshape(1,17)
    scaled_user_vec = scalerUser.transform(user_vec)
    data = json.dumps({"instances":scaled_user_vec[:,3:].tolist()})
    headers = {"content-type": "application/json"}
    json_response = requests.post('http://localhost:8501/v1/models/user_embedding_model:predict', data=data, headers=headers)
    predictions = json.loads(json_response.text)['predictions']
    vu = np.array(predictions)
    
    #compute dot product between user embedding and item embedding
    y_p = np.dot(vms, vu.T)
    y_pu = scalerTarget.inverse_transform(y_p)
    
    #Sort the result
    sorted_index = np.argsort(-y_pu,axis=0).reshape(-1).tolist()  #negate to get largest rating first
    
    #return the top 10 movies
    result = item_vecs[sorted_index[:10],0].astype(int)
    
    return result

app = FastAPI(title='Movie Recommender')

class User(BaseModel):
    uid: int

@app.get("/")
def home():
    return "Congratulations! Your API is working as expected. Now head over to http://localhost:80/docs"

@app.post("/predict") 
def prediction(user: User):

    payload = user.uid
    print('payload is:',payload)
    response = retrieve(payload).tolist()
    print("response is:", response)
    
    return {"Recommended":response}

