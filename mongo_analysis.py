from pymongo import MongoClient

client=MongoClient("mongodb+srv://user1:user123@cluster0.rnd2980.mongodb.net/")

db=client.books_data
document=db.mystery_3.aggregate([
    {"$match":{"Rating":"Four"}}
])

for d in document:
    print(d)