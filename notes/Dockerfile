FROM python:3.10

ADD selenium.py .
COPY requirements.txt .
RUN pip install -r requirements.txt


RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get -y install google-chrome-stable


CMD [ "python", "./selenium.py" ]
