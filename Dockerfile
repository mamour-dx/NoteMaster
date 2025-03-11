FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 5000
COPY . .

CMD [ "streamlit", "run", "app.py" , "--server.port=5000"]