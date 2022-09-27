import os
import discord
import logging
from coffee import coffee_bot
from inspire import get_quote
from encourage import update_encouragement, delete_encouragement, positivity, sad_words
from keep_alive import keep_alive
from replit import db

client = discord.Client(intents = discord.Intents.default())

handler = logging.basicConfig(filename='discord.log', format= '[%(asctime)s] %(levelname)s - %(message)s')

if 'responding' not in db.keys():
	db['responding'] = True

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	msg = message.content
	if msg.startswith('$hello'):
		await message.channel.send("Hello Universe, I'm xosnos' first bot!")
	elif msg.startswith('$coffee'):
		coffee_bot()
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

	if db['responding'] and any(word in msg for word in sad_words):
		await message.channel.send(positivity(msg))

try:
	keep_alive()
	client.run(os.environ['TOKEN'], log_handler=handler, log_level=logging.INFO)
except discord.HTTPException as e:
	logging.error(e)