FROM python:3.11.7-slim-bookworm
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT [ "python","-m","kmua_quote_api" ]