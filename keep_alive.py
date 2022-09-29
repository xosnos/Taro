from flask import Flask
from threading import Thread
import socket

app = Flask('')

@app.route('/')
def home():
	with open('README.md', 'r') as f:
		return f.read()
		
def run():
	app.run(host='0.0.0.0', port=8080)

def port_in_use():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		return s.connect_ex(('0.0.0.0', 8080)) == 0

def keep_alive():
	if not port_in_use():
		t = Thread(target=run)
		t.start()