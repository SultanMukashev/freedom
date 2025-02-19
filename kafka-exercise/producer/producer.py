import json
import random
import time
from kafka import KafkaProducer
from kafka.errors import KafkaError

# Sample stock symbols
stocks = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]

# Initialize a Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['host.docker.internal:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8'),
    retries=5,  # Retries before failing
    request_timeout_ms=20000,  # Increase timeout
    acks='all'  # E
)

# Function to produce stock prices
def produce_stock_prices():
    while True:
        for stock in stocks:
            price = round(random.uniform(100, 500), 2)
            timestamp = int(round(time.time() * 1000))
            message = {'symbol': stock, 'price': price, 'timestamp': timestamp}
            try:
                 producer.send('stock-prices', value=message).get(timeout=10)  # Ensure messages are sent
            except KafkaError as e:
                print(f"Kafka Error: {e}")
            # producer.send('stock-prices', value=message)
            print(f"Sent: {message}")
        time.sleep(1)

produce_stock_prices()