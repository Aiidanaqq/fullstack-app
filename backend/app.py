from flask import Flask, request, jsonify

app = Flask(__name__)

data = []

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(data)

@app.route('/api/data', methods=['POST'])
def add_data():
    item = request.json
    data.append(item)
    return jsonify({"message": "added"}), 201

@app.route('/api/data/<int:index>', methods=['DELETE'])
def delete_data(index):
    if index < len(data):
        data.pop(index)
        return jsonify({"message": "deleted"})
    return jsonify({"error": "not found"}), 404

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
