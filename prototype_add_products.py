import os

from woocommerce import API
from dotenv import load_dotenv


load_dotenv()

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")



def add_to_wp(pr):
    wcapi = API(
        url="https://4.kpipartners.ru",
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        timeout=50,
    )
    response = wcapi.post("products", pr)


