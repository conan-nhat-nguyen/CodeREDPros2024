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

    best_flights = get_best_flights(input)

    # Sort the best_flights by price
    best_flights.sort(key=lambda x: x['price']['total'], reverse=False)

    return jsonify({
        'best_flights': best_flights[:10]
    })


if __name__ == '__main__':
    app.run(debug=True)