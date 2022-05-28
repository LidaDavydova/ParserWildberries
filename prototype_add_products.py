import os
from dotenv import load_dotenv

from woocommerce import API


load_dotenv()

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")

wcapi = API(
    url=URL_OF_YOUR_WP_SITE,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    timeout=50,
)




def add_to_wp(pr):
    wcapi = API(
        url="https://4.kpipartners.ru",
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        timeout=50,
    )
    response = wcapi.post("products", pr)


