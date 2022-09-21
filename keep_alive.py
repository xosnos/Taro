from flask import Flask
from threading import Thread
from time import sleep
from os import system

app = Flask('')

@app.route('/')
def home():
	return """
 		<h1>Taro</h1>
    """

def run():
	app.run(host='0.0.0.0', port=8080)

def keep_alive():
	t = Thread(target=run)
	t.start()

def restart():
	print('restarting')
	sleep(7)
	system('python main.py')