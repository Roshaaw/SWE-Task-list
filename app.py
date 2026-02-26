#To run in terminal python app.py
from flask import Flask, request, render_template, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime


app = Flask(__name__)

# Get Mongo URI from environment variable
MONGODB_URI = "mongodb+srv://roshan_81:RoshB1381@cluster0.clh1f6y.mongodb.net/?appName=Cluster0"
client = MongoClient(MONGODB_URI)

db = client["taskdb"]
tasks_collection = db["tasks"]

@app.route("/")
def index():
    # Sort: unfinished --> finished --> newest first
    tasks = list(tasks_collection.find().sort([("done", 1), ("created_at", -1)]))
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    task_content = request.form.get("task")
    if task_content and task_content.strip():
        tasks_collection.insert_one({"task": task_content, "done": False, "created_at": datetime.utcnow()})
    return redirect("/")

@app.route("/delete/<task_id>")
def delete_task(task_id):
    tasks_collection.delete_one({"_id": ObjectId(task_id)})
    return redirect("/")

@app.route("/toggle/<task_id>")
def toggle_done(task_id):
    task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    if task:
        tasks_collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {"done": not task.get("done", False)}}
        )
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)