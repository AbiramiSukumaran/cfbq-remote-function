import functions_framework
import numpy as np 
import pandas as pd 
from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from flask import jsonify

#Function Definition
@functions_framework.http
def movie_score_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    #Getting input parameters in the format: 'GENRE;RUNTIME'
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'name' in request_json:
        name = request_json['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = 'Thriller;180'

    #Read training file
    train = pd.read_csv('movies_bq_src.csv',  encoding='latin-1')

    #Create a dataframe df with only 2 fields: GENRE and RUNTIME
    df = train[['genre', 'runtime']].copy()

    #Create a dataframe for SCORE, the target variable
    y = train[['score']].copy()
    
    #Converting Categorical Features to encoded values
    genre = pd.get_dummies(df['genre'])
    df.drop(['genre'], axis = 1, inplace = True)
    df = pd.concat([df, genre], axis = 1)

    #Create df X_train and y_train
    X_train = df
    y_train = y

    #Instantiate Logistic Regression and fit the input and target df
    model = LogisticRegression()
    model.fit(X_train, y_train)

    #Split the input parameter into GENRE and RUNTIME values
    y_genre = name.split(";")[0]
    y_runtime = name.split(";")[1]

    # Create dataframe for test data (only copying the columns and not data)
    df_test = pd.DataFrame(columns = df.columns)

    #Create a dict with the values for the test data
    dict = {y_genre:1,
            'runtime':y_runtime
            }

    #Assign dict into the test dataframe and fill other NaN values to 0
    df_test.loc[len(df_test.index)] = dict
    df_test = df_test.fillna(0)

    #Predict score for the test data using the fitted model
    pred = model.predict(df_test)
    res = pred[0]

    #Convert prediction result to string and store it in variable called replies
    replies = [str(res)]

    #JSONify the response output as BigQuery expects it to be a JSON
    return jsonify( { "replies" : replies } )

    #return 'Hello! Score for a {} movie with a runtime of about {} minutes is {}'.format(y_genre, y_runtime, res)
