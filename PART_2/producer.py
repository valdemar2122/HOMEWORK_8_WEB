import pika
from faker import Faker
from models import Contact


credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="127.0.0.1", port=5672, credentials=credentials)
)
channel = connection.channel()

channel.queue_declare(queue="contacts_email")
channel.queue_declare(queue="contacts_SMS")


def generate_contacts(num_contacts):
    fake = Faker()

    for _ in range(num_contacts):
        fullname = fake.name()
        email = fake.email()
        phone_number = fake.phone_number()
        preffered_contact_method = fake.random_element(elements=["SMS", "email"])
        contact = Contact(
            fullname=fullname,
            email=email,
            phone_number=phone_number,
            preffered_contact_method=preffered_contact_method,
        )
        contact.save()
        if preffered_contact_method == "SMS":
            channel.basic_publish(
                exchange="", routing_key="contacts_SMS", body=str(contact.id)
            )
        else:
            channel.basic_publish(
                exchange="", routing_key="contacts_email", body=str(contact.id)
            )
        print(
            f"Contact created: {fullname}, {email}, {phone_number}, {preffered_contact_method}"
        )


generate_contacts(5)
connection.close()
