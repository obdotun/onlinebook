from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# User Service Routes
@app.route('/register', methods=['POST'])
def register():
    response = requests.post('http://localhost:3001/register/', json=request.json)
    return jsonify(response.json()), response.status_code

@app.route('/login', methods=['POST'])
def login():
    response = requests.post('http://localhost:3001/login/', json=request.json)
    return jsonify(response.json()), response.status_code

def validate_token(token):
    # Call the User service to validate the token (for example, using a REST API call)
    # response = requests.post('http://localhost:3001/validate_token/', headers={'Authorization': f'Bearer {token}'})
    print(f'validated token is {token}')
    response = requests.post('http://localhost:3001/validate_token/', headers={'Authorization': token})
    # auth_header = request.headers.get('Authorization')
    # headers = {'Authorization': auth_header}
    # response = requests.post('http://localhost:3001/validate_token/', headers=headers)
    return response.json()['valid']  # Return whether the token is valid

@app.route('/logout', methods=['POST'])
def logout():
    # headers = {'Authorization': request.headers.get('Authorization')}
    # response = requests.post('http://localhost:3001/logout/', json=request.json, headers=headers)
    # return jsonify(response.json()), response.status_code
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return jsonify({"error": "Authorization token is missing"}), 401

    headers = {'Authorization': auth_header}
    response = requests.post('http://localhost:3001/logout/', json=request.json, headers=headers)

    return jsonify(response.json()), response.status_code

@app.route('/profile', methods=['GET'])
def profile():
    headers = {'Authorization': request.headers.get('Authorization')}
    response = requests.get('http://localhost:3001/profile/', headers=headers)
    return jsonify(response.json()), response.status_code

@app.route('/profile', methods=['PUT'])
def update_profile():
    headers = {'Authorization': request.headers.get('Authorization')}
    response = requests.put('http://localhost:3001/profile/', json=request.json, headers=headers)
    return jsonify(response.json()), response.status_code

# Book Service Routes
@app.route('/books', methods=['GET'])
def books():
    response = requests.get('http://localhost:3002/books/')
    return jsonify(response.json()), response.status_code

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    response = requests.get(f'http://localhost:3002/books/{book_id}/')
    return jsonify(response.json()), response.status_code

@app.route('/books', methods=['POST'])
def add_book():
    token = request.headers.get('Authorization')  # Extract token from header
    print(f'book token is {token}')
    if not token or not validate_token(token):  # Validate the token
        return jsonify({"message": "Unauthorized"}), 403  # Unauthorized if token is invalid

    # headers = {'Authorization': request.headers.get('Authorization')}
    response = requests.post('http://localhost:3002/books/', json=request.json)
    return jsonify(response.json()), response.status_code

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    headers = {'Authorization': request.headers.get('Authorization')}
    response = requests.put(f'http://localhost:3002/books/{book_id}/', json=request.json, headers=headers)
    return jsonify(response.json()), response.status_code

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    headers = {'Authorization': request.headers.get('Authorization')}
    response = requests.delete(f'http://localhost:3002/books/{book_id}/', headers=headers)
    return jsonify(response.json()), response.status_code

# Order Service Routes
@app.route('/orders', methods=['POST'])
def orders():
    headers = {'Authorization': request.headers.get('Authorization')}
    response = requests.post('http://localhost:3003/orders/', json=request.json, headers=headers)
    return jsonify(response.json()), response.status_code

@app.route('/orders', methods=['GET'])
def get_orders():
    headers = {'Authorization': request.headers.get('Authorization')}
    response = requests.get('http://localhost:3003/orders/', headers=headers)
    return jsonify(response.json()), response.status_code

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    headers = {'Authorization': request.headers.get('Authorization')}
    response = requests.get(f'http://localhost:3003/orders/{order_id}/', headers=headers)
    return jsonify(response.json()), response.status_code

@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    headers = {'Authorization': request.headers.get('Authorization')}
    response = requests.put(f'http://localhost:3003/orders/{order_id}/', json=request.json, headers=headers)
    return jsonify(response.json()), response.status_code

@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    headers = {'Authorization': request.headers.get('Authorization')}
    response = requests.delete(f'http://localhost:3003/orders/{order_id}/', headers=headers)
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(port=3000)
