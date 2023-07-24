import openai
import requests
import lib.config as config

openai.api_key = config.read('openai', 'api_key')


def get_apod():
    '''Get the Astronomy Picture of the Day from NASA's API'''
    url     = config.read('nasa', 'url')
    api_key = config.read('nasa', 'api_key')

    response = requests.get(url, params={'api_key': api_key})

    return response.json()['hdurl']


def chat(message: str) -> str:
    '''Chat with GPT-3'''
    function_map = {
        'get_apod': get_apod,
    }

    response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[config.read('openai', 'pre_prompt'),{"role": "user", "content": message}],
                functions=config.read('openai', 'functions'),
                function_call='auto'
            )
    
    response_message = response.choices[0]['message']

    if response_message.get('function_call'):
        function_name = response_message['function_call']['name']
        print(response_message)

        return function_map[function_name]()
    
    else:
        return response_message['content']
