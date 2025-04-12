from pymongo import MongoClient

# MongoDB Connection String
MONGO_URI = "mongodb+srv://navita:Rnavita02@cluster0.f1auc.mongodb.net/student_dbs?retryWrites=true&w=majority"
# mongodb://localhost:27017/student_dbs
try:
    client = MongoClient(MONGO_URI)
    db = client["student_dbs"]  # Your database name
    users_collection = db["users"]  # Your collection name
    print("MongoDB Connected Successfully")
except Exception as error:
    print("MongoDB Connection Error:", error)
