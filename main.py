import functions_framework
import numpy as np 
import pandas as pd 
from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from flask import jsonify

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
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'name' in request_json:
        name = request_json['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = 'Thriller;180'


    train = pd.read_csv('movies_bq_src.csv',  encoding='latin-1')
    df = train[['genre', 'runtime']].copy()
    y = train[['score']].copy()
    #Converting Categorical Features
    genre = pd.get_dummies(df['genre'])
    df.drop(['genre'], axis = 1, inplace = True)
    df = pd.concat([df, genre], axis = 1)

    X_train = df
    y_train = y
    model = LogisticRegression()
    model.fit(X_train, y_train)

    y_genre = name.split(";")[0]
    y_runtime = name.split(";")[1]

    # Create test df
    df_test = pd.DataFrame(columns = df.columns)

    dict = {y_genre:1,
            'runtime':y_runtime
            }
    df_test.loc[len(df_test.index)] = dict
    df_test = df_test.fillna(0)

    pred = model.predict(df_test)
    res = pred[0]

    replies = [str(res)]

    return jsonify( { "replies" : replies } )

    #return 'Hello! Score for a {} movie with a runtime of about {} minutes is {}'.format(y_genre, y_runtime, res)
