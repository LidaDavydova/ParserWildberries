ЗАЙТИ В КАТАЛОГ notes!!!
1. В файле selenium1.py в строке url прописываем ссылку бренда
2. Создаем образ из Dockerfile:
docker build -t parser-api .
3. Запускаем образ:
docker run -it parser-api url
Пример: docker run -it parser-api "https://www.wildberries.ru/catalog/elektronika/muzyka-i-video?sort=popular&page=1&fbrand=6108"
