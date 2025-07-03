from pymongo import MongoClient

client=MongoClient("")

db=client.books_data
document=db.mystery_3.aggregate([
    {"$match":{"Rating":"Four"}}
])

for d in document:
    print(d)
