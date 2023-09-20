from flask import Flask, request, jsonify, make_response, render_template
from block import Blockchain

blockchain = Blockchain()

app = Flask(__name__)


def add_headers(output, status_code):
    response = make_response(jsonify(output), status_code)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/write', methods=['POST'])
def write():
    try:
        log_content = request.json['log_content']
        blockchain.add_block(log_content)
        return add_headers({'message': 'block added successfully.'}, 201)
    except Exception as _e:
        return add_headers({'error': str(_e)}, 400)


@app.route('/validate', methods=['GET'])
def validate():
    try:
        if blockchain.is_chain_valid():
            return add_headers({'message': 'The blockchain is valid.'}, 200)
        else:
            return add_headers({'error': 'The blockchain is not valid.'}, 400)
    except Exception as _e:
        return jsonify({'error': str(_e)}), 400


@app.route('/view_blockchain', methods=['GET'])
def view_blockchain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append({
            'index': block.index,
            'previous_hash': block.previous_hash,
            'timestamp': block.timestamp,
            'data': block.data,
            'hash': block.hash
        })
    return add_headers({'length': len(chain_data), 'chain': chain_data}, 200)


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000, threads=5)
