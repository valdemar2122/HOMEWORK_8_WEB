from mongoengine import connect
import configparser


config = configparser.ConfigParser()
config.read("homework8/config.ini")

mongo_user = config.get("MongoDB", "USER")
mongodb_pass = config.get("MongoDB", "PASS")
db_name = config.get("MongoDB", "DB_NAME")
domain = config.get("MongoDB", "DOMAIN")

# connect to cluster on AtlasDB with connection string

connect(
    host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true""",
    ssl=True,
)
