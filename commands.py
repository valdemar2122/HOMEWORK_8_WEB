from models import Quote, Author
import connection


def search_quotes(command):
    if command.startswith("name:"):
        author_name = command[len("name:") :].strip()
        author = Author.objects(fullname__istartswith=author_name).first()
        if author:
            quotes = Quote.objects(author=author).all()
        else:
            print("author not found")
            return
    elif command.startswith("tag:"):
        tag = command.split("tag:")[-1].strip()
        quotes = Quote.objects(tags__icontains=tag).all()

    elif command.startswith("tags: "):
        tags = command[len("tags: ") :].strip().split(",")
        quotes = Quote.objects(tags__in=tags).all()
    else:
        print("Invalid command...")
        return

    for quote in quotes:
        print(quote.to_json().encode("utf-8").decode("unicode-escape"))


def main():
    while True:
        command = input("Enter command to search quotes: ").strip()
        if command == "exit":
            break
        search_quotes(command)


if __name__ == "__main__":
    main()
