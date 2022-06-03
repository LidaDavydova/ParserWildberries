from requests_html import HTMLSession
import os

from woocommerce import API

# from dotenv import load_dotenv


# from prototype_add_products import add_to_wp
# load_dotenv()

# consumer_key = os.getenv("CONSUMER_KEY")
consumer_key = "ck_53ab65e2203636a08a70858b5c4a8af1db8ba0cc"
# consumer_secret = os.getenv("CONSUMER_SECRET")
consumer_secret = "cs_fc6beeed5832747ed21fb088c75a4858aac037f5"


# print(price)


class ProductWB:
    def __init__(self, request):
        # self.product = product
        self.request = request
        self.session = HTMLSession()

    def add_to_model(self, valid_name_product, valid_img, price):
        # print(valid_img)
        model = {
            "name": valid_name_product,
            "regular_price": price,
            "images": [
                {
                    "src": valid_img,
                    "alt": valid_name_product,
                }
            ],
        }
        return model

    def add_to_wp(self, pr):
        wcapi = API(
            url="https://4.kpipartners.ru",
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            timeout=150,
        )
        response = wcapi.post("products", pr)

    def parse_product(self, prod):
        # print(prod.absolute_links)
        i = list(prod.absolute_links)
        for j in i:
            # print(j)
            # for item in prod.absolute_links:
            #     print(item)
            if "lk/basket" in j:
                pass
            else:
                # print(item)
                req = self.session.get(j)
                req.html.render(sleep=2)
                # i = r.html.find("span.price-block__final-price", first=True).text
                # print(item)
                # print("hello")
                price = req.html.xpath(
                    '//*[@id="infoBlockProductCard"]/div[2]/div/div/p/span', first=True
                ).text[:-2]
                # print("hello", price)
                product_name = req.html.xpath(
                    "/html/body/div[1]/main/div[2]/div/div/div[2]/div/div[3]/div[7]/h1",
                    first=True,
                ).text
                if "/" in product_name:
                    product_name = product_name.replace("/", "")
                # print(product_name)
                not_valid_img = req.html.xpath(
                    "/html/body/div[1]/main/div[2]/div/div/div[2]/div/div[1]/div/div[1]/div/div/div[1]/ul/li[1]/div/img",
                    first=True,
                ).attrs["src"]

                valid_img = "https:" + not_valid_img
                model = self.add_to_model(
                    valid_name_product=product_name, valid_img=valid_img, price=price
                )
                # print(model)
                self.add_to_wp(model)
                # print(not_valid_img)

    def get_all_products(self):
        pages = self.request.html.xpath(
            "/html/body/div[1]/main/div[2]/div/div/div[6]/div[1]/div[5]/div/div",
            first=True,
        )
        # print(pages.absolute_links == set())
        if pages.absolute_links != set():
            for page in pages.absolute_links:
                # print(page)
                page_url = self.session.get(page)
                page_url.html.render(sleep=2)

                product = page_url.html.xpath(
                    "/html/body/div[1]/main/div[2]/div/div/div[6]/div[1]/div[4]/div/div",
                    first=True,
                )
                self.parse_product(product)
                # print(prod.absolute_links)
                # product_count.append(*prod.absolute_links)
                # print(len(product_count))
        else:
            product = self.request.html.xpath(
                "/html/body/div[1]/main/div[2]/div/div/div[6]/div[1]/div[4]/div/div",
                first=True,
            )
            self.parse_product(product)
        # return product

        # price = self.get_price()
        # valid_img, valid_name_product = self.parse_img()
        # model = self.add_to_model(product_name, valid_img, price)
        # self.add_to_wp(model)


if __name__ == "__main__":
    print("Введите ссылку для парсинга")
    url = str(input())

    s = HTMLSession()
    r = s.get(url)
    # print("hello")
    # print(r.text)
    r.html.render(sleep=2)
    product_class_object = ProductWB(request=r)
    product_class_object.get_all_products()
    # print("gohor")
