from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# In-memory "database" - list of user dicts
users = [
    {"id":1, "name":"Alice", "email": "alice@gmail.com"},
    {"id":2, "name":"bob", "email": "bob@gmail.com"},
]

def get_next_id():
    """ Return nest user id"""
    if not users:
        return 1
    return max(user["id"] for user in users) + 1 

def find_user(user_id):
    """ Find a user dict by id, or return None..."""
    return next((u for u in users if u["id"] == user_id),None)

# -- ROUTES---

@app.route("/users",methods=["GET"])
def list_users():
    """ Returen list of all Users """
    return jsonify(users), 200

@app.route("/users/<int:user_id>", medhods=["GET"])
def get_user(user_id):
    """ Return a single user by id ."""
    user = find_user(user_id)
    if user is None:
        return jsonify({"error":"User Not Found"}), 404
    return jsonify(user), 200

@app.route("/users", methods=["POST"])
def create_user():
    """ Create a new user. Expect JSON with 'name' and 'email'.. """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": " Both 'name' and 'email' are required"}), 400
    
    # Optional : check for duplicate email

    if any (u["email"] == email for u in users):
        return jsonify({"error": "Email Already exists"}), 400
    
    new_user = {"id": get_next_id(), "name" : name, "email": email}
    users.append(new_user)
    return jsonify(new_user), 201

@app.route("/users/<int:user_id>", methods = ["PUT"])
def update_user(user_id):
    """ Update an existing user (full or partial)"""
    user = find_user(user_id)
    if user is None:
        return jsonify({"error" : "User not found"}), 404
    
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    # Update allowd fields

    name = data.get("name")
    email = data.get("email")

    if name:
        user["name"] = name

    if email:
        # Prevent duplicate email (for simlicity)
        if any(u["email"] == email and u["id"] != user_id for u in users):
            return jsonify({"error": "Email already exists"}), 400
        user["email"] = email

    return jsonify(user), 200

app.route("/users/<int:user_id>", methods = ["DELETE"])
def delete_user(user_id):
    """ Delete a user by id."""
    user = find_user(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    users.remove(user)
    return "", 204  # No content

if __name__ == "__main__":
    # Run the app
    app.run(debug=True)