from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd
import requests

# Initialize Flask app
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def responses():
    response = requests.get(
        'https://raw.githubusercontent.com/labs15-best-places/backend/master/data-seeding/1-cities/data.js')
    return str(response.text)

if __name__ == "__main__":
    app.run(debug=True)