from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import datetime

app = Flask(__name__)

# --- MongoDB connection (config comes from environment variables / k8s secrets) ---
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.environ.get("MONGO_DB_NAME", "todo_app")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client[DB_NAME]
todos_collection = db["todos"]


@app.route("/")
def index():
    todos = list(todos_collection.find().sort("created_at", -1))
    return render_template("index.html", todos=todos)


@app.route("/add", methods=["POST"])
def add_todo():
    task = request.form.get("task", "").strip()
    if task:
        todos_collection.insert_one({
            "task": task,
            "done": False,
            "created_at": datetime.datetime.utcnow()
        })
    return redirect(url_for("index"))


@app.route("/toggle/<todo_id>")
def toggle_todo(todo_id):
    todo = todos_collection.find_one({"_id": ObjectId(todo_id)})
    if todo:
        todos_collection.update_one(
            {"_id": ObjectId(todo_id)},
            {"$set": {"done": not todo["done"]}}
        )
    return redirect(url_for("index"))


@app.route("/delete/<todo_id>")
def delete_todo(todo_id):
    todos_collection.delete_one({"_id": ObjectId(todo_id)})
    return redirect(url_for("index"))


@app.route("/health")
def health():
    # Used by Kubernetes liveness/readiness probes
    try:
        client.admin.command("ping")
        return jsonify({"status": "healthy", "db": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 503


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

