from flask import Flask,request,render_template
import numpy as np
import pandas as pd
import pickle
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "7E6xl1Pfz5kUHEIYNq1VccoIs7v6YR8U90HsDeA6ajBr"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
#payload_scoring = {"input_data": [{"fields":[["GlobalReactivePower","GlobalIntensity","SubmeterReading1","SubmeterReading2","SubmeterReading3"], "values": [array_of_values_to_be_scored, another_array_of_values_to_be_scored]}]}
#model=pickle.load(open('PCASSS_model.pkl','rb'))
app=Flask(__name__)
@app.route('/')
def home():
    return render_template('demo.html')

@app.route('/predict',methods=['GET','POST'])
def predict1():
    GlobalReactivePower = request.form["GlobalReactivePower"]
    GlobalIntensity = request.form["GlobalIntensity"]
    SubmeterReading1= request.form["SubmeterReading1"]
    SubmeterReading2= request.form["SubmeterReading2"]
    SubmeterReading3= request.form["SubmeterReading3"]
    t = [[int(GlobalReactivePower),int(GlobalIntensity),int(SubmeterReading1),int(SubmeterReading2 ),int(SubmeterReading3)]]
    payload_scoring = {"input_data": [{"fields": [["GlobalReactivePower", "GlobalIntensity","SubmeterReading1","SubmeterReading2","SubmeterReading3"]], "values": t}]}
    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/d16b98c0-d4a5-446c-9161-3eaad1825352/predictions?version=2022-03-30', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    input_features=[float(x) for x in request.form.values()]
    features_value=[np.array(input_features)]
    features_name=['Global_reactive_power','Global_intensity','Sub_metering_1','Sub_metering_2','Sub_metering_3']
    df=pd.DataFrame(features_value,columns=features_name)
    output=model.predict(df)
    
    return render_template('result1.html',prediction_text=output)

if __name__ == "__main__" :
        app.run(debug=True)