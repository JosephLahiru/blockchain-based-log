from flask import Flask, request, jsonify, make_response, render_template
from block import Blockchain

blockchain = Blockchain()

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
        print(log_content)
        blockchain.add_block(log_content)

    except Exception as _e:
        return add_headers({'error': str(_e)})


@app.route('/validate', methods=['GET'])
def validate():
    try:
        if blockchain.is_chain_valid():
            return jsonify({'message': 'The blockchain is valid.'}), 200
        else:
            return jsonify({'error': 'The blockchain is not valid.'}), 400
    except Exception as _e:
        return jsonify({'error': str(_e)}), 400


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000, threads=5)
