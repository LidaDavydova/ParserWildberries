FROM python:3.10

ADD req_html.py . 
COPY requirements.txt .
RUN pip install -r requirements.txt



RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' |  tee /etc/apt/sources.list.d/google-chrome.list
RUN apt -y update 
RUN apt -y install google-chrome-stable


CMD [ "python", "./req_html.py" ]

