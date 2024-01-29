from models import Quote, Author
import connection
from redis import Redis
import re

redis_client = Redis(host="localhost", port=6379)


def search_quotes(query_type, query_value):
    cached_result = redis_client.get(f"{query_type}, {query_value}")
    if cached_result:
        cached_result.decode("utf-8")

    if query_type == "name":
        author = Author.objects(fullname__istartswith=query_value).first()
        if author:
            quotes = Quote.objects(author=author)
    elif query_type == "tag":
        quotes = Quote.objects(tags__icontains=query_value)

    elif query_type == "tags":
        tags = query_value.split(",")
        quotes = Quote.objects(tags__in=tags)

    else:
        return "Invalid query type. Please use 'name', 'tag', or 'tags'."

    result = []

    for quote in quotes:
        result.append(f"{quote.author.fullname} : {quote.quote}")

    redis_client.set(f"{query_type} : {query_value}", "\n".join(result))

    return "\n".join(result)


def main():
    while True:
        command = input("Enter command to search quotes: ").strip()
        if command == "exit":
            break

        # Розбивка команди на тип та значення
        match = re.match(r"(\w+):(.+)", command)
        if match:
            query_type = match.group(1).strip()
            query_value = match.group(2).strip()

            # Виклик функції пошуку та виведення результатів
            print(search_quotes(query_type, query_value))
        else:
            print("Invalid command format. Please use 'name:', 'tag:', or 'tags:'.")


if __name__ == "__main__":
    main()
