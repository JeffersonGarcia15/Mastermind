from flask import Blueprint, request
import requests

BASE_URL = "https://www.random.org/integers/?num=4&min=0&max=7&col=1&base=10&format=plain&rnd=new"

game_routes = Blueprint("game", __name__)

sequence = []

@game_routes.route('/start')
def start_game():
    try:
        response = requests.get(BASE_URL)
        # As per the docs: Response.raise_for_status() will raise an HTTPError if the HTTP request returned an unsuccessful status code.
        response.raise_for_status()
        # content-type: text/plain;charset=UTF-8 so since it is not JSON we use .text
        data = response.text.split()
        
        global sequence
        sequence = [int(num) for num in data]

        return {
            "data": [
                {   
                    "game_id": "123",
                }
            ],
            "error": None
        }
    except requests.exceptions.RequestException as error:
        return {
            "data": [],
            "error": str(error)
        }