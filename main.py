from sklearn import tree
from flask import request, Flask, Response
import json
import sys, traceback

class big5():
	def __init__(self, o,c,e,a,n,q):
		self.Openess=o
		self.Conscientiousness=c
		self.Extraversion=e
		self.Agreeableness=a
		self.Neuroticism=n
		self.Profesion=q

	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, indent=4)


class clf():
	def __init__(self, ptree):
		self.tre = ptree
		self.clf = None

features = list()
labels = list()

app = Flask(__name__)
numero = 2
cla = clf(tree.DecisionTreeClassifier())
@app.route("/input/<o>/<c>/<e>/<a>/<n>/<q>", methods = ['POST'])
def index(o,c,e,a,n,q):
	response =  Response(content_type='text/plain', status=403)
	if request.method == 'POST':
		var = [o,c,e,a,n]
		big = big5(o,c,e,a,n,q)
		response = app.response_class(response=big.toJSON(),status=200,mimetype='application/json')
		features.append(var)
		labels.append(q)
		print(features, file=sys.stderr)

	return response

@app.route("/learn", methods=['POST'])
def learn():
	if request.method == 'POST':
		print('llego1', file=sys.stderr)
		print(features, file=sys.stderr)
		print(labels, file=sys.stderr)
		try:
			cla.clf =cla.tre.fit(features, labels)
		except:
			traceback.print_exc(file=sys.stderr)
		return Response(content_type='text/plain', status=200)



@app.route("/predict/<o>/<c>/<e>/<a>/<n>" , methods=['POST'])
def predict(o,c,e,a,n):
	response =  Response(content_type='text/plain', status=403)
	if request.method == 'POST':
		try:
			var = [[o,c,e,a,n]]
			profesion = str(cla.clf.predict(var)[0])
			big = big5(o,c,e,a,n,profesion)
			response = app.response_class(response=big.toJSON(),status=200,mimetype='application/json')
		except:
			traceback.print_exc(file=sys.stderr)
	return response

if __name__ == "__main__":
    app.run(debug=True, port=8000, host='localhost')


