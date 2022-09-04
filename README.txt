ЗАЙТИ В КАТАЛОГ notes!!!
1. Создаем образ из Dockerfile:
docker build -t parser-api .
2. Запускаем образ:
docker run -it parser-api url
url - ссылка бренда/селлера
Пример: docker run -it parser-api "https://www.wildberries.ru/catalog/elektronika/muzyka-i-video?sort=popular&page=1&fbrand=6108"
