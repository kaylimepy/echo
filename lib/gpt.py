import openai
import requests
import json
import lib.config as config

from datetime import datetime

openai.api_key = config.read('openai', 'api_key')


def get_apod(date: str) -> str:
    '''Get the Astronomy Picture of the Day from NASA's API'''
    url     = config.read('nasa', 'url')
    api_key = config.read('nasa', 'api_key')

    response = requests.get(url, params={'api_key': api_key, 'date': date})

    return response.json()['hdurl']


def chat(message: str) -> str:
    '''Chat with GPT-3'''
    function_map = {'get_apod': get_apod}

    response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=__messages(message),
                functions=config.read('openai', 'functions'),
                function_call='auto'
            )
    response_message = response.choices[0]['message']

    if 'function_call' in response_message:
        function_name = response_message['function_call']['name']
        function_args = json.loads(response_message['function_call']['arguments'])

        return function_map[function_name](date=function_args['date'])
    else:
        return response_message['content']

def __messages(message):
    '''Create the messages list for the GPT API'''
    messages = []

    # GPT-3 only has access to the data that it was trained on, and that data has a cuttoff date.. so if we want
    # to be able to talk about the current date, we need to add it to the messages list.
    current_date = f'Todays date is {datetime.now().strftime("%d/%m/%Y")}. Use this date for any date related questions.'

    messages.append(config.read('openai', 'pre_prompt'))
    messages.append({'role': 'system', 'content': current_date})
    messages.append({'role': 'user', 'content': message})

    return messages