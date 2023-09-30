# cfbq-remote-function
A Python Cloud Function to predict the success score of a movie based on its GENRE and RUNTIME is being invoked as a remote function from BIGQUERY. 

1. STEP 1
   Python Cloud Function
   a. create, test (Source code in repo)

2. STEP 2
   Deploy Cloud Function
   a. Open Cloud Shell Editor
   b. Create a new directory in the root, named "movie-score-remote"
   c. Upload the 4 files - main.py, requirements.txt, movies_bq_src.csv and movies_bq_src_predict.csv
   d. Open Cloud Shell Terminal
   e. Run the command: CD movie-score-remote
   f. To deploy the CF, run:
   gcloud functions deploy movie_score_http  --trigger-http --runtime=python311 --gen2
   g: Allow unauthenticated access for now ( technically the recommendation is not to set this, and required to use auth)

3. STEP 3
   Create BigQuery Dataset and Table
  a. Create Dataset named "movies" in BigQuery in the region us-central1 by running the below command in Cloud Shell Terminal:
      bq mk --location=us-central1 movies
  b. Create an External Connection by clicking the ADD button on the top left corner of the BigQuery cosole
  c. Click Connections to external data sources and select Connection Type as "BigLake and remote functions (cloud resource)
  d. Provide the same region as the dataset and click CREATE DATASET
  e. Copy the Service Account in the Connection Configuration page and save it somewhere for later use
  f. Create a table and load data to be predicted: From the Cloud Shell Terminal, run below command:
bq load --source_format=CSV --skip_leading_rows=1 movies.movies_score_predict \
./movies_bq_src_predict.csv \ Id:numeric,name:string,rating:string,genre:string,year:numeric,released:string,score:string,director:string,writer:string,star:string,country:string,budget:numeric,company:string,runtime:numeric,data_cat:string

4. STEP 4
   Create Remote Functions
   a. Open Query Editor in BigQuery console and enter the following command to create the remote function:

CREATE OR REPLACE FUNCTION movies.predict_score(x STRING) RETURNS STRING
REMOTE WITH CONNECTION `<<YOUR_PROJECT>>.us-central1.cloud-fun-conn`
OPTIONS (
  endpoint = '<<YOUR_DEPLOYED_CF_URL>>'
);

  b. Now that the model is created. you can use test your remote function. Run the following SQL:
  SELECT name, genre, runtime, 
`<<YOUR_PROJECT>>.movies`.predict_score(concat(genre,';', runtime)) as predicted_score
from `<<YOUR_PROJECT>>.movies.movies_score_predict`;

c. You should see the result like this:
**name               genre   runtime   predicted_score**
Charlie's Angels     Action   98       7

REMEMBER:

1. This is a batch prediction method
2. Your Cloud Function response (return response) should be in the format of JSON with string array set to the response variable "replies".
   return_json = jsonify( { "replies":  replies } )
   return return_json

References:

https://cloud.google.com/bigquery/docs/remote-functions




