from mongoengine import StringField, EmailField, BooleanField, Document
from connection import connect


class Contact(Document):
    fullname = StringField(required=True)
    email = EmailField(required=True)
    phone_number = StringField(required=True)
    preffered_contact_method = StringField(choices=["SMS", "email"], default="email")
    message_sent = BooleanField(default=False)
