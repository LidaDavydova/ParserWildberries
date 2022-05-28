import os

from woocommerce import API




def add_to_wp(pr):
    wcapi = API(
        url="https://4.kpipartners.ru",
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        timeout=50,
    )
    response = wcapi.post("products", pr)


