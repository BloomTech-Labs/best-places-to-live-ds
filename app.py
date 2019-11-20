from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np
import pandas as pd
import requests
import numpy as np
import json

df1 = pd.read_csv('ranked_df.csv')
photos_df = pd.read_csv('photos.csv')

# Function to return list of top cities
def rankify(df, factors, top=20, quant=.60):
    df_copy = df
    for i in factors:
        df_copy = df_copy[df[i] > df_copy[i].quantile(quant)]
    df_copy['score'] = df_copy[factors].mean(axis=1)
    df_copy = df_copy.sort_values('score', ascending=False)
    return df_copy['name'].head(top).tolist()

def city_output(df, cities):
    # make a copy of the dataframe
    df_copy = df

    # truncate the dataframe row-wise to only the cities in the input
    df2 = df_copy.loc[df['name'].isin(cities)]

    # initialize columns to be masked
    columns = ['name', 'population', 'photoWeb', 'photoMobile']

    # truncate the dataframe column-wise to the ones in 'columns'
    df3 = df2[columns]

    # return the dataframe in dictionary form
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
    jd = json.dumps(data, ensure_ascii=False)
    data_array = json.loads(jd)
    factors = (data_array['input1'])
    #print(factors)

    # Call the rankify function to return top 10 cities
    cities = rankify(df1, factors)
    #print(cities)

    dict1 = city_output(df1, cities)
 
    return jsonify(dict1)


@app.route('/', methods=['POST', 'GET'])
def responses():
    response = requests.get(
        'https://raw.githubusercontent.com/labs15-best-places/backend/master/data-seeding/1-cities/data.js')
    
    return str(response.text)



if __name__ == "__main__":
    app.run(debug=True)