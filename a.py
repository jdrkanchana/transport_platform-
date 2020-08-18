from flask import Flask, render_template, request

a=0
app = Flask(__name__)


@app.route('/')
def index():
    return 'Server Works!'

@app.route('/zone', methods=['POST'])
def zone():
	b=1
	global a
	if b>0:
		a=5
		print(a)
	else:
		a=4
		print(a)

def save(a):
	b=a+2
	print(b)