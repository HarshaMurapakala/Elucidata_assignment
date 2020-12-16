from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

data= 0
file= 0

@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('index.html')

@app.route('/data', methods=['GET', 'POST'])
def data():
	if request.method == 'POST':
		file = request.form['upload-file']
		global data,file
		data = pd.read_csv(file)
		x= data[data["Accepted Compound ID"].str.endswith(" PC", na=False)]
		x.to_csv("ends_with_pc.csv")
		y= data[data["Accepted Compound ID"].str.endswith("LPC", na=False)]
		y.to_csv("ends_with_lpc.csv")
		z= data[data["Accepted Compound ID"].str.endswith("plasmalogen", na=False)]
		z.to_csv("ends_with_plasmalogen.csv")
		return render_template('data.html')
		#,data=x.to_html())

@app.route('/roundoff', methods=['GET', 'POST'])
def roundoff():
	if request.method == 'POST':
		global data
		temp = data["Retention time (min)"].round()
		data.insert(loc=2, column= "Retention Time Roundoff (in mins)", value= temp)
		data.to_csv(file)
		return render_template('roundoff.html')


@app.route('/mean', methods=['GET', 'POST'])
def mean():
	if request.method == 'POST':
		global data
		x= data.groupby("Retention Time Roundoff (in mins)").mean()
		x= x.iloc[:, 3:]
		x.to_csv("mean.csv")
		return render_template('mean.html')




if __name__ == '__main__':
	app.run(debug=True)