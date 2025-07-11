from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB connection — replace with your Mongo URI
client = MongoClient("mongodb://localhost:27017")
db = client["mydatabase"]
collection = db["items"]

# Create
@app.route("/items", methods=["POST"])
def create_item():
    data = request.json
    result = collection.insert_one(data)
    return jsonify({"_id": str(result.inserted_id)}), 201

# Read All
@app.route("/items", methods=["GET"])
def get_items():
    items = []
    for item in collection.find():
        item["_id"] = str(item["_id"])
        items.append(item)
    return jsonify(items)

# Read One
@app.route("/items/<item_id>", methods=["GET"])
def get_item(item_id):
    item = collection.find_one({"_id": ObjectId(item_id)})
    if item:
        item["_id"] = str(item["_id"])
        return jsonify(item)
    else:
        return jsonify({"error": "Item not found"}), 404

# Update
@app.route("/items/<item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.json
    result = collection.update_one(
        {"_id": ObjectId(item_id)},
        {"$set": data}
    )
    if result.matched_count:
        return jsonify({"message": "Item updated"})
    else:
        return jsonify({"error": "Item not found"}), 404

# Delete
@app.route("/items/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    result = collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count:
        return jsonify({"message": "Item deleted"})
    else:
        return jsonify({"error": "Item not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
