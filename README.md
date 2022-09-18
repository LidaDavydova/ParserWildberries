<h1> Parsing data the catalog of brand/seller wildberries.ru</h1>

<h3>For parsing data you need to do these steps:</h3>

1. Create image from Dockerfile:<br>
	docker build -t parser-api .
2. Run image:<br>
	docker run -it parser-api <url of brand/seller><br>
Example: docker run -it parser-api "https://www.wildberries.ru/catalog/elektronika/muzyka-i-video?sort=popular&page=1&fbrand=6108"
