import requests
from flask import Flask, request, jsonify, make_response, render_template

app = Flask(__name__)

def add_headers(output):
    response = make_response(jsonify(output))
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/write', methods=['POST'])
def write():
    try:
        log_content = request.json['log_content']

    except Exception as _e:
        return add_headers({'error': str(_e)})


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000, threads=5)
