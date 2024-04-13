from flask import Flask, request, jsonify
from flask_cors import CORS
from aitest import AI
from werkzeug.utils import secure_filename
from pydub import AudioSegment
import os
import random

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return '{"World": "hello"}'

@app.route('/post_json', methods=['POST'])
def process_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        a = json['a']
        b = json['b']
        answer = AI.do_any(a, b)
        return f'{{"answer":"{answer}"}}'
    else:
        return 'Content-Type not supported!'

@app.route('/post_params', methods=['POST'])
def process_params():
    a = request.args.get('a', None)
    b = request.args.get('b', None)
    answer = AI.do_any(a, b)
    return f'{{"answer":"{answer}"}}'

@app.route('/file', methods=['POST'])
def process_files():
    print("Пошло")
    isSuccess = False
    if 'soundFile' not in request.files:
        print("Не работает")
        return jsonify({"IsSuccess": isSuccess, "Message": "No file part"})

    file = request.files['soundFile']  # according to the name you append to formdata

    if file:  # and allowed_file(file.filename):
        filename = secure_filename(file.filename).replace(".mp3", '', 1)
        print(filename)
        file.save(os.path.join(os.getcwd(), "static", f"sound_{filename}.mp3"))
        sound = AudioSegment.from_mp3(f"/static/sound_{filename}.mp3")
        print("Popalo 2")
        sound.export(f"/static/sound_{filename}.wav", format="wav")
        os.remove(f"/static/sound_{filename}.mp3")
        isSuccess = True
        tasks = []
        return jsonify({"Synth": random.randint(0, 100), "Not_Synth": random.randint(0, 100)})
        # return jsonify({"IsSuccess": isSuccess, "tasks": tasks})

if __name__ == "__main__":
    app.run()