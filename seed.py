import json
import connection
from models import Author, Quote

# Зчитуємо дані з файлів JSON та зберігаємо у базу даних
with open("authors.json", "r") as file:
    authors_data = json.load(file)

with open("quotes.json", "r") as file:
    quotes_data = json.load(file)

# Зберігаємо дані авторів у колекції Author
for author_data in authors_data:
    author = Author(**author_data)
    author.save()

# Зберігаємо дані цитат у колекції Quote
for quote_data in quotes_data:
    author_fullname = quote_data.pop("author")
    author = Author.objects(fullname=author_fullname).first()
    quote_data["author"] = author
    quote = Quote(**quote_data)
    quote.save()
