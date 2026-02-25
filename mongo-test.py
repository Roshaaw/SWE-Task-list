from pymongo import MongoClient
import os

MONGODB_URI = "mongodb+srv://roshan_81:RoshB1381@cluster0.clh1f6y.mongodb.net/?appName=Cluster0"
client = MongoClient(MONGODB_URI)

db = client["taskdb"]
collection = db["tasks"]

# --- WRITE (insert test task) ---
collection.insert_one({"task": "Test Task from mongo-test.py"})

for task in collection.find():
    print(task)
