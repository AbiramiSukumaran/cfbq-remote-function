# cfbq-remote-function
A Python Cloud Function to predict the success score of a movie based on its GENRE and RUNTIME, is being invoked as a remote function from BIGQUERY. 

**#To try this demo, access developer credits from here:
https://gcpcredits.com/codevipa**

**Sign up for Innovator's Champion: [https://cloud.google.com/innovators?utm_source=cloud_sfdc&utm_medium=email&utm_campaign=FY23-1H-vipassana-innovators&utm_content=joininnovators&utm_term=-](url)**

**1. STEP 1**

   Python Cloud Function: create, test (Source code in repo)
   a. Open Cloud Shell Editor
   b. Create a new directory in the root, named "movie-score-remote"
   Open Cloud Shell Terminal and run below command:
   git clone https://github.com/AbiramiSukumaran/cfbq-remote-function movie-score-remote
   c. This command should upload the 4 files - main.py, requirements.txt, movies_bq_src.csv and movies_bq_src_predict.csv

**2. STEP 2**
   Deploy Cloud Function
   a. Open Cloud Shell Terminal
   b. Run the command:
   cd movie-score-remote
   c. To deploy the CF, run:
   gcloud functions deploy movie_score_http  --trigger-http --runtime=python311 --gen2
   Note:
    1. Enter 27 as the numerical choice for region
    2. Allow unauthenticated access for now, not recommended (The recommendation is to use OAUTH2)

**3. STEP 3**
   Create BigQuery Dataset and Table
  a. Create Dataset named "movies" in BigQuery in the region us-central1 by running the below command in Cloud Shell Terminal:

bq mk --location=us-central1 movies_pc

  b. Create an External Connection by clicking the ADD button on the top left corner of the BigQuery cosole
  
  c. Click Connections to external data sources and select Connection Type as "BigLake and remote functions (cloud resource)
  
  d. Provide the same region as the dataset (us-central1) and click CREATE DATASET
  
  e. Copy the Service Account in the Connection Configuration page and save it somewhere for later use
  
  f. Create a table and load data to be predicted: From the Cloud Shell Terminal, run below command:


bq load --source_format=CSV --skip_leading_rows=1 movies_pc.movies_score_predict \
./movies_bq_src_predict.csv \ Id:numeric,name:string,rating:string,genre:string,year:numeric,released:string,score:string,director:string,writer:string,star:string,country:string,budget:numeric,company:string,runtime:numeric,data_cat:string

**4. STEP 4**
   Create Remote Functions
   a. Open Query Editor in BigQuery console and enter the following command to create the remote function:

CREATE OR REPLACE FUNCTION movies_pc.predict_score(x STRING) RETURNS STRING
REMOTE WITH CONNECTION `<<YOUR_PROJECT>>.us-central1.cloud-fun-conn`
OPTIONS (
  endpoint = '<<YOUR_DEPLOYED_CF_URL>>'
);

**5. STEP 5**
   Predict
   
  a. Now that the model is created. you can use test your remote function. Run the following SQL:
  
  SELECT name, genre, runtime, 
`<<YOUR_PROJECT>>.movies_pc`.predict_score(concat(genre,';', runtime)) as predicted_score
from `<<YOUR_PROJECT>>.movies_pc.movies_score_predict`;

  b. You should see the result like this:
**name               genre   runtime   predicted_score**
Charlie's Angels     Action   98       7

**REMEMBER:**

1. This is a batch prediction method
2. Your Cloud Function response (return response) should be in the format of JSON with string array set to the response variable "replies".
   return_json = jsonify( { "replies":  replies } )
   return return_json

References:

https://cloud.google.com/bigquery/docs/remote-functions




