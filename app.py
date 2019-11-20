from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np
import pandas as pd
import requests
import numpy as np
import json

df1 = pd.read_csv('ranked_df.csv')


def rankify(df, factors, top=20, quant=.60):
    df_copy = df
    for i in factors:
        df_copy = df_copy[df[i] > df_copy[i].quantile(quant)]
    df_copy['score'] = df_copy[factors].mean(axis=1)
    df_copy = df_copy.sort_values('score', ascending=False)
   
    # truncate df row-wise to top 20 cities 
    df_copy = df_copy.head(top)
    
    df_copy['photoWeb'] = df_copy['photoWeb'].replace({pd.np.nan: None})
    df_copy['photoMobile'] = df_copy['photoMobile'].replace({pd.np.nan: None})
    
    # initialize columns to be masked
    columns = [
               'name', 
               'population', 
               'photoWeb', 
               'photoMobile', 
               'id',
               'short_name',
               'state'
               ]

    # truncate the dataframe column-wise to the ones in 'columns'
    df2 = df_copy[columns]

    return df2.to_dict(orient='record')

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
 
    return jsonify(cities)


@app.route('/', methods=['POST', 'GET'])
def responses():
    response = requests.get(
        'https://raw.githubusercontent.com/labs15-best-places/backend/master/data-seeding/1-cities/data.js')
    
    return str(response.text)



if __name__ == "__main__":
    app.run(debug=True)