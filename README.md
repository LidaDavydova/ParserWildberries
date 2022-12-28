<h1> Parsing data the catalog of brand/seller wildberries.ru to WordPress</h1>

<h3>For parsing data you need to do these steps:</h3>

1. Change your data in app.py from plagin woocommerce: consumer_key, consumer_secret, url to wordpress site
![image](https://user-images.githubusercontent.com/79317010/209855567-e755bd88-1201-4a16-8035-238f43bc4020.png)

2. Create image from Dockerfile:<br>
	docker build -t parser-api .
3. Run image:<br>
	docker run -it parser-api <url of brand/seller><br>
Example: docker run -it parser-api "https://www.wildberries.ru/catalog/elektronika/muzyka-i-video?sort=popular&page=1&fbrand=6108"

