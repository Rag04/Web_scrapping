import scrapy
from pymongo import MongoClient
from pathlib import Path
import datetime

client= MongoClient("mongodb+srv://user1:user123@cluster0.rnd2980.mongodb.net/")
db=client.books_data

def insert(page,title,image,rating,price,availability):
    collection=db[page]
    doc={
        "title":title,
        "image":image,
        "Rating":rating,
        "price":price,
        "availability":availability,
        "date": datetime.datetime.now(tz=datetime.timezone.utc),
    }
    ins=collection.insert_one(doc)
    return ins.inserted_id
    
class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["toscrape.com"]
    start_urls = ["https://toscrape.com"]

    async def start(self):
        urls = [
            "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
            "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"books-{page}.html"
        # Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")

        card=response.css(".product_pod")

        for item in card:
            title=item.css("h3>a::text").get()
            print(title)
            image=item.css(".image_container img")
            image=image.attrib['src'].replace("../../../../media","https://books.toscrape.com/media")
            print(image)
            rating= item.css(".star-rating").attrib['class'].split(" ")[1]
            print(rating)
            price=item.css(".price_color::text").get()
            print(price)
            availability = item.css('.availability::text').getall()
            availability = ''.join(availability).strip() #to remove \n
            print(availability)

            insert(page,title,image,rating,price,availability)
