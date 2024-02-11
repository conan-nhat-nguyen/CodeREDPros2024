import requests
from converter import *
from prompt_to_json import *
import asyncio

def get_flight_url(departure_city, destination_city, departure_date, return_date=None):
    departure_id_array = city_converter(departure_city)

    destination_id_array = city_converter(destination_city)
    departure_date = date_format(departure_date)
    if (return_date): return_date = date_format(return_date) 

    url_array = []
    for departure_id in departure_id_array:
        for destination_id in destination_id_array:
            url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={departure_id}&destinationLocationCode={destination_id}&departureDate={departure_date}&adults=1&nonStop=false&max=250"
            if (return_date): url += f"&returnDate={return_date}"
            url_array.append(url)

    return url_array

async def main():
    token_flight = "hSAHjug5w2OjWLoqhfXx8GALQtZL"

    headers_flight = {"Authorization" : "Bearer " + token_flight}


    user_data = extract_to_json("I want to book a flight from Houston to New York on May 6th 2024")

    user_data = user_data['text']

    print(user_data)

    await asyncio.sleep(2)

    req_url_array = get_flight_url(user_data['departure'], user_data['destination'], user_data['departure_date'])


    best_flights_all = []

    for req_url in req_url_array:
        response_flight = requests.get(req_url, headers=headers_flight)
        best_flights_all += response_flight.json()['data'][:2]


    print(len(best_flights_all))

asyncio.run(main())