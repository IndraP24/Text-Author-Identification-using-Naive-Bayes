from flask import Flask, request
import flasgger
from flasgger import Swagger
import pickle

import sys
sys.path.append('/home/indrap24/Desktop/Projects/All Projects/Text-Author-Identification-using-Naive-Bayes')
from author_identifier.util import *


with open("../author_identifier/artifacts/text_author_identifier/model_artifact.pkl", "rb") as f:
    model_artifact = pickle.load(f)
    f.close()

app = Flask(__name__)
Swagger(app)

@app.route("/")
def home():
    return "<h1>Welcome</h1>  <p> Using this api you can perform an author identification task. <br><br> You can input a dialogue of your choice and the api will let you know if the dialogue is more likely to be uttered by Captain America or Iron Man <br> <br> A naive bayes classifier was built on the transcript of Captain America: The first avenger and Iron Man and conditional probabilities of different words were obtained for these two characters. The <u>predict_dialogue</u> endpoint let's you try this out, so go ahead and try it out!</p>"

@app.route("/predict_dialogue", methods = ["POST"])
def predict_dialogue():
    """This endpoint predicts whether a given dialogue is more likely to be spoken by Cap or Stark
    ---
    parameters:
      - name: text
        in: query
        type: string
        required: true
      
    responses:
        200:
            description: Who is more likely to speak these words, Rogers or Stark
        
    """
    text = request.args.get("text")
    prediction = utils.predict(str(text), model_artifact["probabilites"], model_artifact["log_prior"])

    return f"This dialogue is more likely to have come from {prediction[0]}."