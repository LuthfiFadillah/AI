import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.model_selection import train_test_split, cross_val_predict, KFold
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn import metrics
from sklearn.model_selection import cross_val_predict
from sklearn.externals import joblib
from werkzeug.utils import secure_filename
from flask import send_from_directory
import pandas as pd


app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py
UPLOAD_FOLDER = '/home/nim_13515098/Documents/IF Semester 5/ai/markingat'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt'])

app.config.from_envvar('MARKINGAT_SETTINGS', silent=True)

@app.route('/')
def show_homepage():
	return render_template('HomePage.html')

@app.route('/form')
def show_form():
	return render_template('FillFormPage.html')

@app.route('/upload', methods=['GET','POST'])
def upload_file():
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			# flash('No file part')
			return redirect(request.url)
		file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
		if file.filename == '':
			# flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('uploaded_file', filename=filename))
	return render_template('UploadPage.html')

@app.route('/credits')
def show_credit():
	return render_template('CreditsPage.html')

# @app.route('/result', methods=['POST'])
# def show_result():
# 	return render_template('ResultPage.html')

@app.route('/result', methods=['GET'])
def process_form():
	age = float(request.args.get('age'))
	workclass = float(request.args.get('workclass'))
	fnlwgt = float(request.args.get('fnlwgt'))
	education = float(request.args.get('education'))
	education_num = float(request.args.get('education_num'))
	marital_status = float(request.args.get('marital_status'))
	occupation = float(request.args.get('occupation'))
	relationship = float(request.args.get('relationship'))
	race = float(request.args.get('race'))
	sex = float(request.args.get('sex'))
	capital_gain = float(request.args.get('capital_gain'))
	capital_loss = float(request.args.get('capital_loss'))
	hours_per_week = float(request.args.get('hours_per_week'))
	native_country = float(request.args.get('native_country'))

	test_input = {'age':[age], 'workclass':[workclass], 'fnlwgt':[fnlwgt],
	 'education':[education], 'education_num':[education_num], 'marital_status':[marital_status], 
	 'occupation':[occupation], 'relationship':[relationship], 'race':[race], 'sex':[sex], 'capital_gain':[capital_gain], 
	 'capital_loss':[capital_loss], 'hours_per_week':[hours_per_week], 'native_country':[native_country]}

	pd_test_input = pd.DataFrame(data=test_input)


	MLP = joblib.load('MLP.model')
	result = MLP.predict(pd_test_input)
	if (result[0] == 1):
		result_message = "> 50"
	else:
		result_message = "<= 50"

	return render_template('ResultPage.html', value=result_message)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS	

@app.route('/uploads/<filename>')
def uploaded_file(filename):
	arrMap = [0, {'State-gov': 0, 'Self-emp-not-inc': 1, 'Private': 2, 'Federal-gov': 3, 'Local-gov': 4, 'nan': 5, 'Self-emp-inc': 6, 'Without-pay': 7, 'Never-worked': 8}, 0, {'Bachelors': 0, 'HS-grad': 1, '11th': 2, 'Masters': 3, '9th': 4, 'Some-college': 5, 'Assoc-acdm': 6, 'Assoc-voc': 7, '7th-8th': 8, 'Doctorate': 9, 'Prof-school': 10, '5th-6th': 11, '10th': 12, '1st-4th': 13, 'Preschool': 14, '12th': 15}, 0, {'Never-married': 0, 'Married-civ-spouse': 1, 'Divorced': 2, 'Married-spouse-absent': 3, 'Separated': 4, 'Married-AF-spouse': 5, 'Widowed': 6}, {'Adm-clerical': 0, 'Exec-managerial': 1, 'Handlers-cleaners': 2, 'Prof-specialty': 3, 'Other-service': 4, 'Sales': 5, 'Craft-repair': 6, 'Transport-moving': 7, 'Farming-fishing': 8, 'Machine-op-inspct': 9, 'Tech-support': 10, 'nan': 11, 'Protective-serv': 12, 'Armed-Forces': 13, 'Priv-house-serv': 14}, {'Not-in-family': 0, 'Husband': 1, 'Wife': 2, 'Own-child': 3, 'Unmarried': 4, 'Other-relative': 5}, {'White': 0, 'Black': 1, 'Asian-Pac-Islander': 2, 'Amer-Indian-Eskimo': 3, 'Other': 4}, {'Male': 0, 'Female': 1}, 0, 0, 0, {'United-States': 0, 'Cuba': 1, 'Jamaica': 2, 'India': 3, 'nan': 4, 'Mexico': 5, 'South': 6, 'Puerto-Rico': 7, 'Honduras': 8, 'England': 9, 'Canada': 10, 'Germany': 11, 'Iran': 12, 'Philippines': 13, 'Italy': 14, 'Poland': 15, 'Columbia': 16, 'Cambodia': 17, 'Thailand': 18, 'Ecuador': 19, 'Laos': 20, 'Taiwan': 21, 'Haiti': 22, 'Portugal': 23, 'Dominican-Republic': 24, 'El-Salvador': 25, 'France': 26, 'Guatemala': 27, 'China': 28, 'Japan': 29, 'Yugoslavia': 30, 'Peru': 31, 'Outlying-US(Guam-USVI-etc)': 32, 'Scotland': 33, 'Trinadad&Tobago': 34, 'Greece': 35, 'Nicaragua': 36, 'Vietnam': 37, 'Hong': 38, 'Ireland': 39, 'Hungary': 40, 'Holand-Netherlands': 41}, 0, 0, 0, 0, 0, 0]
	test1 = pd.read_csv(send_from_directory(app.config['UPLOAD_FOLDER'],filename), header=None, na_values=["?"], skipinitialspace=True, usecols=list(range(0,14)), comment='|')
	for i in range(14):
		if( (i != 0) and (i != 2) and (i != 4) and (i != 10) and (i != 11) and (i != 12) ):
			test1 = mapping_test(test1, i, arrMap[i])
	MLP = joblib.load('MLP.model')
	result = MLP.predict(test1)
	return render_template('ResultPage.html', value=result)



def mapping_test(df, target_column, mapping):
    df_mod = df.copy()
    df_mod[target_column] = df_mod[target_column].replace(mapping)
    df_mod[target_column] = df_mod[target_column].tolist()
    df_mod[target_column] = [int(y) for y in df_mod[target_column]]
    return (df_mod)

