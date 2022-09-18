h1 Parsing data from brend's/seller's catalog wildberries.ru
***

For parsing data you need to do these steps:

1. Create image from Dockerfile:
	docker build -t parser-api .
2. Run image:
	docker run -it parser-api url
	url - brend's/seller's url
	Example: docker run -it parser-api "https://www.wildberries.ru/catalog/elektronika/muzyka-i-video?sort=popular&page=1&fbrand=6108"
