
from flask import Flask, jsonify, request, flash, render_template
from sklearn.externals import joblib
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

# 
@app.route('/')
def index():
	return render_template('index.html')


@app.route('/apply')
def forms():
	return render_template('forms.html')


def predict(input_list):
	model = joblib.load('model.pkl')
	result = model.predict(input_list)
	return result[0]


@app.route('/result', methods=['POST'])
def contact():

	# if form.validate() == False:
	# 	flash('Field required')
	# else:

	input_list = request.form.to_dict()
	name = input_list.pop('Name')
	data = pd.DataFrame(input_list, index=[0])
	input_list_v = list(data.values)

	y_pred = predict(input_list_v)
	print("prediction", y_pred)
	if y_pred == 1:
		prediction = 'Approved'
	elif y_pred == 0:
		prediction = 'Rejected'
		# return jsonify({'clasd': prediction})
	return render_template('result.html', prediction=prediction, name=name, input_list=input_list)



if __name__=='__main__':
	app.run(debug=True)
