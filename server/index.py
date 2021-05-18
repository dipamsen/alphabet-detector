import pickle
from flask import Flask, jsonify, request
from flask_cors import CORS
clf = pickle.load(open("model.lr", 'rb'))
from PIL import Image
import numpy as np

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
  return {'m': 'Flask API: Alphabet Detection'}


@app.route('/predict', methods=['POST'])
def predict():
  try:
    file = request.files['upl']
    img = Image.open(file).convert('L').resize((30, 22), Image.ANTIALIAS)
    sample = (np.array(img) / 255)  # .reshape(1, 660)
    prediction = clf.predict(sample.reshape(1, 660))
    Image.fromarray(sample * 255).convert(
        'RGB')  # .save("hello.png", format="png")
    print(prediction)
    return {'test': "ing", "pred": list(prediction)}
  except Exception as e:
    print(e)
    return {'error': "SOMETHING WAS WRONG"}


if __name__ == '__main__':
  app.run()
