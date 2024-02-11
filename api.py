# app/routes.py
from flask import Flask, render_template, jsonify, request
from Amadeus import *
from speech_to_text.speech_to_text import audio_to_input

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 


@app.route('/')
def home():
    return render_template('index.html', message='This is a message')


@app.route('/send', methods=['POST'])
def send():
    input = json.loads(request.data)['inputText']


    try:
        best_flights = get_best_flights(input)
    except Exception as e:
        print(e, flush=True)

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

@app.route('/record', methods=['POST'])
def record():

    request_data = request.files

    print(request_data, flush=True)
    # audio.save('./speech_to_text/audio.wav')


    # transcript = audio_to_input()

    # return {
    #     'ok': True,
    #     'transcription': transcript
    # }
    return {
        'ok': True,
        'transcription': "Hello"
    
    }


if __name__ == '__main__':
    app.run(debug=True)