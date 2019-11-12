from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd
import requests
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer

df1 = pd.read_csv('sm_normalized.csv')

#reduced_df = df[df['population'] >= 93298]


# Function to return list of top cities
def rankify(df, factors, top=10, quant=.75):
    df_copy = df
    for i in factors:
        df_copy = df_copy[df[i] > df_copy[i].quantile(quant)]
    df_copy['score'] = df_copy[factors].mean(axis=1)
    df_copy.sort_values('score', ascending=False) 
    return df_copy['name'].head(top).tolist()



city_data = {
    "input1": "cost_of_living",
    "input2": "median-age"
}

# Initialize Flask app
app = Flask(__name__)


@app.route('/api', methods=['POST', 'GET'])
def city():
    
    # retrieve json user input data
    #data = request.get_json(force=True)

    # Extract factors from JSON and put them in a list
    factors = []
    for key, value in city_data:
        factors.append(value)
        return factors
    
    # Call the rankify function to return top 10 cities
    cities = rankify(df1, factors)

    return cities


@app.route('/', methods=['POST', 'GET'])
def responses():
    response = requests.get(
        'https://raw.githubusercontent.com/labs15-best-places/backend/master/data-seeding/1-cities/data.js')
    
    return str(response.text)

if __name__ == "__main__":
    app.run(debug=True)