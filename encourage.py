import random
from replit import db

sad_words = ['sad', 'depressed', 'unhappy', 'angry', 'miserable', 'depressing']
starter_encouragements = ['Cheer up!', 'Hang in there!', 'You are a great person!']

def update_encouragement(e_message):
	if 'encouragements' in db.keys():
		encouragements = db['encouragements']
		encouragements.append(e_message)
		db['encouragements'] = encouragements
	else:
		db['encouragements'] = [e_message]

def delete_encouragement(index):
	encouragements = db['encouragements']
	if index < len(encouragements):
		del encouragements[index]
	db['encouragements'] = encouragements

def positivity(msg):
	options = starter_encouragements
	
	if 'encouragements' in db.keys():
		options = options + list(db['encouragements'])
	return random.choice(options)