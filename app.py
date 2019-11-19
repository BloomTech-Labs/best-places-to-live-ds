from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np
import pandas as pd
import requests
import numpy as np
import json

df1 = pd.read_csv('ranked_df.csv')

#reduced_df = df[df['population'] >= 93298]


# Function to return list of top cities
def rankify(df, factors, top=20, quant=.60):
    df_copy = df
    for i in factors:
        df_copy = df_copy[df[i] > df_copy[i].quantile(quant)]
    df_copy['score'] = df_copy[factors].mean(axis=1)
    df_copy = df_copy.sort_values('score', ascending=False)
    return df_copy['name'].head(top).tolist()

def city_output(df, cities):
    df_copy = df
    df2 = df_copy.loc[df['name'].isin(cities)]
    columns = ['name', 'population', 'photo']
    df3 = df2[columns]
    return df3.to_dict(orient='record')


city_data = {
    "input1": ["population", "avg_commute_time"]
}

# Initialize Flask app
app = Flask(__name__)
CORS(app)


@app.route('/api', methods=['POST', 'GET'])
def city():
    
    # retrieve json user input data
    data = request.get_json(force=True)

    # Extract factors from JSON and put them in a list
    '''
    factors = []
    for key, value in city_data:
        factors.append(value)
        return list(factors)
    print(factors)
    '''
    #print(city_data)

    jd = json.dumps(data, ensure_ascii=False)
    data_array = json.loads(jd)
    factors = (data_array['input1'])
    #print(factors)

    # Call the rankify function to return top 10 cities
    cities = rankify(df1, factors)
    #print(cities)

    dict1 = city_output(df1, cities)
    #for city in cities:


    return jsonify(dict1)


@app.route('/', methods=['POST', 'GET'])
def responses():
    response = requests.get(
        'https://raw.githubusercontent.com/labs15-best-places/backend/master/data-seeding/1-cities/data.js')
    
    return str(response.text)



if __name__ == "__main__":
    app.run(debug=True)