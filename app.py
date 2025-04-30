from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)

auth = HTTPBasicAuth()

users = {
    "user1": "password1",
    "user2": "password2",
    "admin": "admin"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

@app.route('/')
def home():
    return "Hello, Flask!"

items = []

@app.route('/items', methods=['GET'])
@auth.login_required
def get_items():
    return jsonify(items)

@app.route('/items', methods=['POST'])
@auth.login_required
def create_item():
    data = request.get_json()
    items.append(data)
    return jsonify(data), 201

@app.route('/items/<int:item_id>', methods=['PUT'])
@auth.login_required
def update_item(item_id):
    data = request.get_json()
    if 0 <= item_id < len(items):
        items[item_id].update(data)
        return jsonify(items[item_id])
    return jsonify({"error": "Item not found"}), 404

@app.route('/items/<int:item_id>', methods=['DELETE'])
@auth.login_required
def delete_item(item_id):
    if 0 <= item_id < len(items):
        removed = items.pop(item_id)
        return jsonify(removed)
    return jsonify({"error", "Item not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)