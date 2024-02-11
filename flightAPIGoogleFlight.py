from serpapi import GoogleSearch
from dotenv import dotenv_values
from prompt_to_json import extract_to_json
from id_converter import *

config = dotenv_values(".env")

params = {
    "api_key": config['FLIGHT_API'],
    "engine": "google_flights",
    "hl": "en",
    "gl": "us",
    "departure_id": "CDG",
    "arrival_id": "AUS",
    "outbound_date": "2024-02-11",
    "return_date": "2024-02-17",
    "currency": "USD"
}

search = GoogleSearch(params)
results = search.get_dict()

print(results.keys())

i = 1
for offer in results['best_flights']:
    print(f"Offer {i}:")
    for flight in offer['flights']:
        print(flight['airline'], flight['duration'])
    i+=1