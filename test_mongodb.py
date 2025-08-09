from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://Username:<@password>@cluster0.u3vpox4.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri)

try:
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB!")
except Exception as e:
    print("❌ Connection error:", e)