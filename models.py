from mongoengine import Document, StringField, ListField, ReferenceField, ObjectIdField


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField()

    author_id = ObjectIdField("Author")
