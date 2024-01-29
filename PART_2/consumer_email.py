import pika
import sys
from models import Contact


def main():
    credentials = pika.PlainCredentials("guest", "guest")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue="contacts_email")

    def callback(ch, method, properties, body):
        contact_id = body.decode("utf-8")
        contact = Contact.objects(id=contact_id).first()
        if contact:
            print(
                f"Processing email contact: {contact.fullname}, {contact.email}, {contact.preffered_contact_method}"
            )

            contact.message_sent = True
            contact.save()

    channel.basic_consume(
        queue="contacts_email", on_message_callback=callback, auto_ack=True
    )

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(0)
