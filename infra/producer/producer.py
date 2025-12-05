from kafka import KafkaProducer
import time
import json
import requests

API_KEY = "d4nufppr01qk2nue1jfgd4nufppr01qk2nue1jg0"
BASE_URL = "https://finnhub.io/api/v1/quote"
SYMBOLS = ["AAPL", "MSFT", "TSLA", "GOOGL", "AMZN"]

producer = KafkaProducer(
    bootstrap_servers=["localhost:29092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def fetch_quote(symbol):
    try:
        url = f"{BASE_URL}?symbol={symbol}&token={API_KEY}"
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        data["symbol"] = symbol
        data["timestamp"] = int(time.time())
        return data
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

if __name__ == "__main__":
    print("Producer started...")

    while True:
        for symbol in SYMBOLS:
            q = fetch_quote(symbol)
            if q:
                print("Producing:", q)
                producer.send("stock-quotes", value=q)

        time.sleep(6)
