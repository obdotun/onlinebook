from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    response = requests.post('http://localhost:3001/register/', json=request.json)
    return jsonify(response.json()), response.status_code

@app.route('/books', methods=['GET'])
def books():
    response = requests.get('http://localhost:3002/books/')
    return jsonify(response.json()), response.status_code

@app.route('/books', methods=['POST'])
def add_books():
    response = requests.post('http://localhost:3002/books/', json=request.json)
    return jsonify(response.json()), response.status_code

@app.route('/orders', methods=['POST'])
def add_order():
    response = requests.post('http://localhost:3003/orders/', json=request.json)
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(port=3000)
