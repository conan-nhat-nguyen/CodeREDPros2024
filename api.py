# app/routes.py
from flask import Flask, render_template, jsonify, request
from Amadeus import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', message='This is a message')

@app.route('/send', methods=['POST'])
def send():
    input = json.loads(request.data)['inputText']


    try:
        best_flights = get_best_flights(input)
    except:
        return jsonify({
            'ok': False,
            'message': "Can you provide more information? I need a departure city, a destination city, and a departure date to find a flight."
        })


    # Sort the best_flights by price
    best_flights.sort(key=lambda x: x['price']['grandTotal'], reverse=False)

    return jsonify({
        'ok': True,
        'best_flights': best_flights[:10]
    })


if __name__ == '__main__':
    app.run(debug=True)