import requests
import json


def get_quote():
	response = requests.get('https://zenquotes.io/api/random')
	json_data = json.loads(response.text)
	return '\"{quote}\" - {author}'.format(quote=json_data[0]['q'], author=json_data[0]['a'])