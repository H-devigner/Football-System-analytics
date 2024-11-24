from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, col
import mysql.connector  # Use MySQL connector instead of psycopg2
from dotenv import load_dotenv
import os



#kafka environment variables
# INPUT_TOPIC = os.getenv('INPUT_TOPIC_NAME')
INPUT_TOPIC = "input-topic"
# OUTPUT_TOPIC = os.getenv('OUTPUT_TOPIC_NAME')
# OUTPUT_TOPIC = os.getenv('OUTPUT_TOPIC_NAME')

# Mysql connection details
DATABASE_HOST = "mysql-football"
DATABASE_PORT = "3306"
# Environment variables
# DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_NAME = "football"

# DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_USER = "houcine"

# DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_PASSWORD = "houcine"

# Initialize Spark session
spark = SparkSession.builder \
    .appName("KafkaSparkIntegration") \
    .config("spark.executor.memory", "4g") \
    .config("spark.executor.cores", "2") \
    .config("spark.driver.memory", "4g") \
    .config("spark.driver.cores", "2") \
    .getOrCreate()

# Read from Kafka
kafka_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:29092") \
    .option("subscribe", "input-topic") \
    .load()

# Process the Kafka stream
processed_df = kafka_df.selectExpr("CAST(value AS STRING) as message")

# Function to write each batch to MySQL
def write_to_mysql(batch_df, batch_id):
    try:
        # Establish connection to MySQL
        conn = mysql.connector.connect(
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            database=DATABASE_NAME,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD
        )
        cursor = conn.cursor()

        # Insert each message into the table created using the django naming convention
        for row in batch_df.collect():
            cursor.execute("INSERT INTO django_app_messages(message) VALUES (%s);", (row['message'],))
        conn.commit()

        cursor.close()
        conn.close()
        print("Batch inserted into MySQL")
    except mysql.connector.Error as e:
        print("Failed to connect to MySQL:", e)

# Write stream to MySQL
query = processed_df.writeStream \
    .foreachBatch(write_to_mysql) \
    .outputMode("append") \
    .start()

query.awaitTermination()
