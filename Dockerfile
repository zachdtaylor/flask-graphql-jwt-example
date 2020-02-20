FROM ubuntu:18.04

RUN apt-get update -y && apt-get install -y python3-pip python3-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

ENV AUTH0_DOMAIN 'dev-xy2tjdsq.auth0.com'
ENV API_AUDIENCE 'https://jwttest/api'

ENTRYPOINT ["python3"]

CMD ["app.py"]
