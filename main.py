import os
import discord
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client(intents = discord.Intents.default())

sad_words = ['sad', 'depressed', 'unhappy', 'angry', 'miserable', 'depressing']

starter_encouragements = ['Cheer up!', 'Hang in there!', 'You are a great person!']

if 'responding' not in db.keys():
	db['responding'] = True

def get_quote():
	response = requests.get('https://zenquotes.io/api/random')
	json_data = json.loads(response.text)
	return '\"{quote}\" - {author}'.format(quote=json_data[0]['q'], author=json_data[0]['a'])

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

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	msg = message.content
	if msg.startswith('$hello'):
		await message.channel.send('Hello Universe!')
	elif msg.startswith('$inspire'):
		await message.channel.send(get_quote())
	elif msg.startswith('$new '):
		e_message = msg.split('$new ', 1)[1]
		update_encouragement(e_message)
		await message.channel.send('New encouraging message added.')
	elif msg.startswith('$del'):
		if 'encouragements' in db.keys():
			index = int(msg.split('$del', 1)[1])
			delete_encouragement(index)
		await message.channel.send(list(db['encouragements']))
	elif msg.startswith('$list'):
		if 'encouragements' in db.keys():
			await message.channel.send(list(db['encouragements']))
	elif msg.startswith('$responding'):
		value = msg.split('$responding ', 1)[1]
		if value.lower() == 'true':
			db['responding'] = True
			await message.channel.send('Responding is on.')
		else:
			db['responding'] = False
			await message.channel.send('Responding is off.')

	if db['responding']:
		options = starter_encouragements
		if 'encouragements' in db.keys():
			options = options + list(db['encouragements'])
	
		if any(word in msg for word in sad_words):
			await message.channel.send(random.choice(options))

keep_alive()
client.run(os.environ['TOKEN'])