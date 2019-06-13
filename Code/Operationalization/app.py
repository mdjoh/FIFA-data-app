from flask import Flask, render_template, request
from sklearn.externals import joblib
import os
import pandas as pd
import numpy as np

app = Flask(__name__, static_url_path='/static/')


@app.route('/')
def form():
    return render_template('index.html')

@app.route('/overall')
def firstForm():
	return render_template('firstForm.html')

@app.route('/rate_prediction')
def secondForm():
	return render_template('secondForm.html')

@app.route('/overall/overall_prediction',methods=['POST', 'GET'])
def overall_prediction():

	#get the parameters
	position = int(request.form['name'])-1
	year = float(request.form['year'])
	df=pd.read_excel('../../Data/Processed/Data_with_Potential.xlsx')
	name = str(df.iloc[position,0])
	df=df[df['Name']==name]
	print(df)
	age = year + df['Age'].tolist()[0]
	potential = df['Potential'].tolist()[0]
	current_rate = df['Overall'].tolist()[0]
	# group similar positions together
	forward = ['RS', 'LS', 'RF', 'LF', 'CF', 'ST']

	attack_mid = ['RAM', 'LAM', 'CAM']
	wings = ['RM', 'RW', 'LM', 'LW']

	central_mid = ['CM', 'LCM', 'RCM']
	defensive_mid = ['CDM', 'LDM', 'RDM']

	fullback = ['RB', 'RWB', 'LB', 'LWB']
	cb_def = ['CB', 'LCB', 'RCB']

	gk = ['GK']

	position = df['Position'].tolist()[0]

	if position in forward:
		model = joblib.load('../../Data/Model/Forward_Model.pkl')
	elif position in attack_mid:
		model = joblib.load('../../Data/Model/am_Model.pkl')
	elif position in wings:
		model = joblib.load('../../Data/Model/Wings_Model.pkl')
	elif position in central_mid:
		model = joblib.load('../../Data/Model/Cm_Model.pkl')
	elif position in defensive_mid:
		model = joblib.load('../../Data/Model/Dm_Model.pkl')
	elif position in fullback:
		model = joblib.load('../../Data/Model/Fullback_Model.pkl')
	elif position in cb_def:
		model = joblib.load('../../Data/Model/Cb_Model.pkl')
	elif position in gk:
		model = joblib.load('../../Data/Model/Gk_Model.pkl')


	prediction = model.predict([[age,potential]])
	predicted_overall = prediction.round(1)[0]

	return render_template('rateresults.html', name=str(name),  age=int(age), potential=int(potential), current_rate = current_rate, predicted_rate=int(predicted_overall))



@app.route('/predict_overall', methods=['POST', 'GET'])
def predict_overall():
    # get the parameters
    age = float(request.form['age'])
    
    # load the model and predict
    model = joblib.load('model/linear_regression.pkl')
    prediction = model.predict([[bedrooms, bathrooms, sqft_living15, grade, condition]])
    predicted_price = prediction.round(1)[0]

    return render_template('results.html',
                           bedrooms=int(bedrooms),
                           bathrooms=int(bathrooms),
                           sqft_living15=int(sqft_living15),
                           grade=int(grade),
                           condition=int(condition),
                           predicted_price="{:,}".format(predicted_price)
                           )


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=8080, debug = True)
