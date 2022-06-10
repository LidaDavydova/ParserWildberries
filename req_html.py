from requests_html import HTMLSession
import os

import time
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
    def __init__(self, request, url):
        # self.product = product
        self.request = request
        self.session = HTMLSession()
        self.success_post_count = 0
        self.all_post_count = 0
        self.url = url

    def add_to_model(
        self,
        valid_name_product,
        valid_img,
        alt_img,
        price,
        valid_second_img,
        alt_second_img,
        valid_third_img,
        alt_third_img,
    ):
        # print(valid_img)
        model = {
            "name": valid_name_product,
            "regular_price": price,
            "images": [
                {
                    "src": valid_img if valid_img != "hello" else None,
                    "alt": alt_img if alt_img != "ok" else None,
                },
                {
                    "src": valid_second_img if valid_second_img != "hello"
                    # else None,  # valid_img,
                    else valid_img,
                    "alt": alt_second_img if alt_second_img != "ok"
                    # else None,  # alt_img,
                    else alt_img,
                },
                {
                    "src": valid_third_img if valid_third_img != "hello"
                    # else None,  # valid_img,
                    else valid_img,
                    # "alt": alt_third_img if alt_third_img != "ok" else None,  # alt_img,
                    "alt": alt_third_img if alt_third_img != "ok" else alt_img,
                },
            ],
        }
        return model

    def add_to_wp(self, pr):
        wcapi = API(
            url="https://4.kpipartners.ru",
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            timeout=2500,
        )
        response = wcapi.post("products", pr)

        status = response.status_code
        # self.all_post_count += 1
        if status >= 400:
            # print(self.success_post_count)
            time.sleep(5)
            response = wcapi.post("products", pr)
            # print(response.status_code)
            if response.status_code < 400:
                self.success_post_count += 1
                # print(self.success_post_count)
            # print(response)
        else:
            self.success_post_count += 1
        # print(self.success_post_count)
        # print(self.all_post_count)

    def get_src_and_alt_image(self, tag_position, req):
        try:
            not_valid_img = req.html.xpath(
                f"/html/body/div[1]/main/div[2]/div/div/div[2]/div/div[1]/div/div[1]/div/div/div[1]/ul/li[{tag_position}]/div/img",
                first=True,
            ).attrs["src"]
            valid_img = "https:" + not_valid_img
            alt_img = req.html.xpath(
                f"/html/body/div[1]/main/div[2]/div/div/div[2]/div/div[1]/div/div[1]/div/div/div[1]/ul/li[{tag_position}]/div/img",
                first=True,
            ).attrs["alt"]
            return valid_img, alt_img
        except AttributeError:
            # time.sleep(5)
            # print("None")
            return "hello", "ok"

    def parse_product(self, prod):
        # print(prod.absolute_links)
        i = list(prod.absolute_links)
        self.all_post_count += len(prod.absolute_links) - 1
        for j in i:
            # print(j)
            # for item in prod.absolute_links:
            #     print(item)
            if "lk/basket" in j:
                pass
            else:
                # print(item)
                req = self.session.get(j)
                try:
                    req.html.render(sleep=1, timeout=450)
                except:
                    time.sleep(5)
                    # print("Таймаут рендера страницы. Повторное подключения")
                    req.html.render(sleep=2, timeout=450)

                # i = r.html.find("span.price-block__final-price", first=True).text
                # print(item)
                # print("hello")
                try:
                    price = req.html.xpath(
                        '//*[@id="infoBlockProductCard"]/div[2]/div/div/p/span',
                        first=True,
                    ).text[:-2]
                    # print("hello", price)
                    product_name = req.html.xpath(
                        "/html/body/div[1]/main/div[2]/div/div/div[2]/div/div[3]/div[7]/h1",
                        first=True,
                    ).text
                except:
                    time.sleep(5)
                    r = self.session.get(self.url)
                    r.html.render(sleep=2, timeout=500)
                    price = r.html.xpath(
                        '//*[@id="infoBlockProductCard"]/div[2]/div/div/p/span',
                        first=True,
                    ).text[:-2]
                    # print("hello", price)
                    product_name = r.html.xpath(
                        "/html/body/div[1]/main/div[2]/div/div/div[2]/div/div[3]/div[7]/h1",
                        first=True,
                    ).text
                if "/" in product_name:
                    product_name = "/".join(
                        str(product_name) for product_name in product_name.split("/")
                    )
                # print(product_name)
                # print(j)
                valid_img, alt_img = self.get_src_and_alt_image(1, req)
                valid_second_img, alt_second_img = self.get_src_and_alt_image(2, req)

                valid_third_img, alt_third_img = self.get_src_and_alt_image(3, req)

                model = self.add_to_model(
                    valid_name_product=product_name,
                    alt_second_img=alt_second_img,
                    alt_third_img=alt_third_img,
                    valid_img=valid_img,
                    alt_img=alt_img,
                    valid_second_img=valid_second_img,
                    valid_third_img=valid_third_img,
                    price=price,
                )
                # print(model)
                self.add_to_wp(model)

                # print(not_valid_img)

    def get_all_products(self):
        # pages = self.request.html.xpath(
        #     "/html/body/div[1]/main/div[2]/div/div/div[6]/div[1]/div[5]/div/div",
        #     first=True,
        # )
        # pages = self.request.html.find("div.product-card-list", first=True)
        pages = self.request.html.find(
            "div.pageToInsert.pagination__wrapper", first=True
        )
        # print(pages.absolute_links == set())
        if pages != None:
            if pages.absolute_links != set():
                for page in pages.absolute_links:
                    # print(page)
                    page_url = self.session.get(page)
                    try:
                        page_url.html.render(sleep=1, timeout=150)
                    except:
                        time.sleep(5)
                        page_url.html.render(sleep=2, timeout=150)

                    # product = page_url.html.xpath(
                    #     "/html/body/div[1]/main/div[2]/div/div/div[6]/div[1]/div[4]/div/div",
                    #     first=True,
                    # )
                    product = self.request.html.find(
                        "div.product-card-list", first=True
                    )
                    if product != None:
                        self.parse_product(product)
                    else:
                        time.sleep(5)
                        page_url.html.render(sleep=2, timeout=150)
                        product = self.request.html.find(
                            "div.product-card-list", first=True
                        )
                        self.parse_product(product)
                    # print(prod.absolute_links)
                    # product_count.append(*prod.absolute_links)
                    # print(len(product_count))
            else:
                # product = self.request.html.xpath(
                #     "/html/body/div[1]/main/div[2]/div/div/div[6]/div[1]/div[4]/div/div",
                #     first=True,
                # )
                product = self.request.html.find("div.product-card-list", first=True)
                if product != None:
                    if product.absolute_links != set():
                        self.parse_product(product)
                    else:
                        time.sleep(10)
                        product = self.request.html.find(
                            "div.product-card-list", first=True
                        )
                        if product != None:
                            if product.absolute_links != set():
                                self.parse_product(product)
                else:
                    time.sleep(10)
                    product = self.request.html.find(
                        "div.product-card-list", first=True
                    )
                    if product != None:
                        if product.absolute_links != set():
                            self.parse_product(product)
        else:
            # print("ok")
            product = self.request.html.find("div.product-card-list", first=True)
            if product != None:
                if product.absolute_links != set():
                    self.parse_product(product)
                else:
                    time.sleep(10)
                    product = self.request.html.find(
                        "div.product-card-list", first=True
                    )
                    if product != None:
                        if product.absolute_links != set():
                            self.parse_product(product)
            else:
                time.sleep(10)
                product = self.request.html.find("div.product-card-list", first=True)
                if product != None:
                    if product.absolute_links != set():
                        self.parse_product(product)
        print(f"Загружено {self.success_post_count} из {self.all_post_count}")
        # self.add_to_wp(model)


def count_slashes(url):
    slash_count = 0
    for symbol in url:
        if symbol == "/":
            slash_count += 1
    return slash_count


def validate_url_if_not_catalog_only(url):
    if "=" in url:
        return True
    elif "seller" in url:
        return True
    elif "promotions" in url:
        return True
    elif "brands" in url:
        return True

    elif not url.endswith("/"):
        print("ok")
        url += "/"
        count = count_slashes(url)
        return False if count == 5 else True

    else:
        print("hello")
        count = count_slashes(url)
        return False if count == 5 else True
    # if count == 4:
    #     return False


if __name__ == "__main__":
    print("Введите ссылку для парсинга")
    url = str(input())
    catalog_check = validate_url_if_not_catalog_only(url)
    if catalog_check:
        s = HTMLSession()
        r = s.get(url)
        # print("hello")
        # print(r.text)
        try:
            r.html.render(sleep=2, timeout=450)
        except:
            r.html.render(sleep=1, timeout=450)
        product_class_object = ProductWB(request=r, url=url)
        product_class_object.get_all_products()
    else:
        print("can not copy from main catalog")
