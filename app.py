from flask import Flask, render_template, request
from sklearn.externals import joblib
import os
import pandas as pd
import numpy as np

app = Flask(__name__, static_url_path='/static/')


@app.route('/')
def form():
    return render_template('index.html')

@app.route('/future_rate_prediction')
def firstForm():
	return render_template('firstForm.html')



@app.route('/future_rate_prediction/overall_prediction',methods=['POST', 'GET'])
def overall_prediction():

	#get the parameters
	position = int(request.form['name'])-1
	year = float(request.form['year'])
	df=pd.read_excel('Data/Processed/Data_with_Potential.xlsx')
	name = str(df.iloc[position,0])
	df=df[df['Name']==name]
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
		model = joblib.load('Data/Model/Future/Forward_Model.pkl')
	elif position in attack_mid:
		model = joblib.load('Data/Model/Future/am_Model.pkl')
	elif position in wings:
		model = joblib.load('Data/Model/Future/Wings_Model.pkl')
	elif position in central_mid:
		model = joblib.load('Data/Model/Future/Cm_Model.pkl')
	elif position in defensive_mid:
		model = joblib.load('Data/Model/Future/Dm_Model.pkl')
	elif position in fullback:
		model = joblib.load('Data/Model/Future/Fullback_Model.pkl')
	elif position in cb_def:
		model = joblib.load('Data/Model/Future/Cb_Model.pkl')
	elif position in gk:
		model = joblib.load('Data/Model/Future/Gk_Model.pkl')


	prediction = model.predict([[age,potential]])
	predicted_overall = prediction.round(1)[0]

	return render_template('future_rate_prediction.html', name=str(name),  age=int(age), potential=int(potential), current_rate = current_rate, predicted_rate=int(predicted_overall))


@app.route('/current_rate_prediction')
def secondForm():
	return render_template('secondForm.html')

@app.route('/current_rate_prediction/overall_prediction', methods=['POST', 'GET'])
def current_overall_prediction():
	#get the parameters
	Dribbling = float(request.form['Dribbling'])
	SprintSpeed = float(request.form['SprintSpeed'])
	ShortPassing = float(request.form['ShortPassing'])
	LongPassing = float(request.form['LongPassing'])
	Strength = float(request.form['Strength'])
	position = str(request.form['Position'])
	# group similar positions together
	forward = ['RS', 'LS', 'RF', 'LF', 'CF', 'ST']

	attack_mid = ['RAM', 'LAM', 'CAM']
	wings = ['RM', 'RW', 'LM', 'LW']

	central_mid = ['CM', 'LCM', 'RCM']
	defensive_mid = ['CDM', 'LDM', 'RDM']

	fullback = ['RB', 'RWB', 'LB', 'LWB']
	cb_def = ['CB', 'LCB', 'RCB']

	gk = ['GK']

	if position in forward:
		model = joblib.load('Data/Model/Current/Forward_Model.pkl')
	elif position in attack_mid:
		model = joblib.load('Data/Model/Current/am_Model.pkl')
	elif position in wings:
		model = joblib.load('Data/Model/Current/Wings_Model.pkl')
	elif position in central_mid:
		model = joblib.load('Data/Model/Current/Cm_Model.pkl')
	elif position in defensive_mid:
		model = joblib.load('Data/Model/Current/Dm_Model.pkl')
	elif position in fullback:
		model = joblib.load('Data/Model/Current/Fullback_Model.pkl')
	elif position in cb_def:
		model = joblib.load('Data/Model/Current/Cb_Model.pkl')
	elif position in gk:
		model = joblib.load('Data/Model/Current/Gk_Model.pkl')


	prediction = model.predict([[Dribbling,SprintSpeed,ShortPassing,LongPassing,Strength]])
	predicted_overall = prediction.round(1)[0]

	return render_template('current_rate_prediction.html',position=str(position), Dribbling=int(Dribbling),  SprintSpeed=int(SprintSpeed), ShortPassing=int(ShortPassing), LongPassing = int(LongPassing), Strength=int(Strength),predicted_overall=predicted_overall)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=8080, debug = True)
