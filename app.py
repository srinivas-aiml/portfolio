from flask import Flask, jsonify, request

app = Flask(__name__)

items = {}
next_item_id = 1


@app.get("/")
def index():
    return jsonify({"message": "Simple Items API", "endpoints": ["/items"]})


@app.get("/items")
def list_items():
    return jsonify(list(items.values()))


@app.post("/items")
def create_item():
    global next_item_id

    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not data.get("name"):
        return jsonify({"error": "A non-empty 'name' is required"}), 400

    item = {"id": next_item_id, "name": data["name"]}
    items[next_item_id] = item
    next_item_id += 1
    return jsonify(item), 201


@app.get("/items/<int:item_id>")
def get_item(item_id):
    item = items.get(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item)


@app.put("/items/<int:item_id>")
def update_item(item_id):
    item = items.get(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not data.get("name"):
        return jsonify({"error": "A non-empty 'name' is required"}), 400

    item["name"] = data["name"]
    return jsonify(item)


@app.delete("/items/<int:item_id>")
def delete_item(item_id):
    if items.pop(item_id, None) is None:
        return jsonify({"error": "Item not found"}), 404
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)