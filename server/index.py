import pickle
from flask import Flask
from flask_cors import CORS

app = Flask()
CORS(app)

if __name__ == 'main':
  app.run()
