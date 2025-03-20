import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import flask
from flask import request, jsonify
from flask_cors import CORS

from sklearn.linear_model import Ridge
from sklearn.cluster import KMeans

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.datasets import make_classification
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score

import joblib

app = flask.Flask(__name__)
CORS(app)
#app.config["DEBUG"] = True

def load_data():
	data  = pd.read_csv('./AB_NYC_2019_clean.csv')
	return data

def normalize_price(price):
    min_value = 0
    max_value = 825
    price = price*(max_value - min_value) + min_value

    return price

def clean_data(data,model_name):
    X_train, X_test, y_train, y_test = None, None, None, None

    if(model_name == 'ridge'):
        X = data.drop(columns=['price','name','host_name','neighbourhood']).to_numpy()
        y = data['price'].to_numpy()

        nan_rows = np.any(pd.isna(X), axis=1)
        X = X[~nan_rows]
        y = y[~nan_rows]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    return X_train, X_test, y_train, y_test

def price_predictor(cluster_data):
    ridge_reg = joblib.load('ridge_regression_model.joblib')
    X = cluster_data.drop(columns=['price','name','host_name','neighbourhood']).to_numpy()
    # check the clustered values and predict prices
    price_pred = ridge_reg.predict(X)
    price_pred = normalize_price(price_pred)
    cluster_data = cluster_data.drop(columns=['price'])
    # put the predicted price in the cluster data
    cluster_data['estimated_price'] = price_pred
    # return cluster data
    return cluster_data
    ## TODO

def encode_neighbourhood(neighbourhood_group):
    neigh_maps = {'bronx':0,'brooklyn':1,'manhattan':2,'queens':3,'staten island':4}
    return neigh_maps[neighbourhood_group]

def encode_room_type(room_type):
    room_maps = {'entire home/apt':0,'private room':1,'shared room':2}
    return room_maps[room_type]

def normalize_nights(minimum_nights):
    max_value = 74
    min_value = 1

    return (minimum_nights-min_value)/(max_value-min_value)

@app.route('/hotelRecommendations',methods=['GET'])
def recommend_places():

    # QUERY
    #grp = bronx
    neighbourhood_group = request.args.get('grp')
    #room_type = entire home/apt
    room_type = request.args.get('room')
    #nights = 4
    min_nights = int(request.args.get('nights'))

    # one hot encode the attrs.
    neighbourhood_group = encode_neighbourhood(neighbourhood_group)
    neigh_one_hot = [0]*5
    neigh_one_hot[neighbourhood_group] = 1

    room_type = encode_room_type(room_type)
    room_one_hot = [0]*3
    room_one_hot[room_type] = 1

    # normalize the minimum nights
    min_nights = normalize_nights(min_nights)
    user_details = np.array([neigh_one_hot + room_one_hot + [min_nights]])

    # Load data
    data = load_data()

    X = data[['neighbourhood_group_bronx', 'neighbourhood_group_brooklyn', 'neighbourhood_group_manhattan',
    'neighbourhood_group_queens','neighbourhood_group_staten island','room_type_entire home/apt',
    'room_type_private room', 'room_type_shared room', 'minimum_nights']]

    # Load the clusters
    kmeans = joblib.load('kmeans_model.joblib')
    # Take the users details. Use the following attributes: neighbourhood_grp, room_type and min_nights
    mean_min_nights = 7.029
    std_min_nights = 20.5

    # Find the cluster that is most suitable for the given data point
    labels = kmeans.predict(X)

    predicted_cluster = kmeans.predict(user_details)
    # Load the clusters 
    cluster_data = data[labels == predicted_cluster]
    
    #sorted_indices = np.argsort(distances)
    cluster_data = price_predictor(cluster_data)
    # Convert neighbourhood_group and room_type to labels
    cluster_data['neighbourhood'] = cluster_data[['neighbourhood_group_bronx', 'neighbourhood_group_brooklyn', 'neighbourhood_group_manhattan',
    'neighbourhood_group_queens']].idxmax(axis=1).apply(lambda x: x.replace('neighbourhood_group_', ''))
    cluster_data['room_type'] = cluster_data[['room_type_entire home/apt',
    'room_type_private room', 'room_type_shared room']].idxmax(axis=1).apply(lambda x: x.replace('room_type_', ''))

    cluster_data = cluster_data[['name','host_name','neighbourhood','room_type','estimated_price']]
    
    return jsonify(cluster_data[:100].to_dict('list')),200

if __name__ == '__main__':
    #app.debug=True
    app.run()
