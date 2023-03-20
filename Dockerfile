FROM python:3.10
RUN pip install --upgrade pip
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["waitress-serve", "--listen=0.0.0.0:8080" ,"main:server"]