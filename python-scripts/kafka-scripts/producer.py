import os
import requests
from kafka import KafkaProducer
import time
from dotenv import load_dotenv

# Configuration
API_URL = 'http://api.football-data.org/v4/'
API_KEY = os.getenv('API_KEY')
KAFKA_BROKER = 'kafka:29092'  # Match the Kafka bootstrap server from the consumer script
KAFKA_TOPIC = os.getenv('INPUT_TOPIC_NAME')

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: v.encode('utf-8')
)

def fetch_data_from_api(endpoint):
    """
    Fetch data from the Football Data API.
    """
    headers = {'X-Auth-Token': API_KEY}
    try:
        response = requests.get(API_URL + endpoint, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error fetching data from API: {e}')
        return None

def produce_data_into_kafka(data):
    """
    Produce data to Kafka topic.
    """
    try:
        producer.send(KAFKA_TOPIC, value=str(data))
        print(f'Produced data to Kafka: {data}')
    except Exception as e:
        print(f'Error producing data to Kafka: {e}')

def main():
    """
    Main function to fetch data and produce it to Kafka.
    """
    endpoints = ['competitions/PL']  # Specify the desired endpoint
    while True:
        for endpoint in endpoints:
            data = fetch_data_from_api(endpoint)
            if data:
                produce_data_into_kafka(data)
        # produce_data_into_kafka('data')
        time.sleep(6)  # Wait 60 seconds before making another API request

if __name__ == '__main__':
    main()
