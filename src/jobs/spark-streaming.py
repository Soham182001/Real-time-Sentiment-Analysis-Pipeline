import pyspark
from pyspark.sql import SparkSession
from huggingface_hub import InferenceClient
from time import sleep
import os
from pyspark.sql.functions import col, from_json, when, udf
from pyspark.sql.types import StructType, StringType, StructField, FloatType
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import config


# Remove jupyter-specific settings since we're not using Jupyter
os.environ['SPARK_HOME'] = '/Users/ganeshmedewar/Desktop/Spark/Spark'
os.environ['PYSPARK_PYTHON'] = 'python'
os.environ["JAVA_HOME"] = '/Library/Java/JavaVirtualMachines/jdk-17.jdk/Contents/Home'
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.0 pyspark-shell'




client = InferenceClient(
    provider="featherless-ai",
    api_key=config['openai']['api_key'],
)

def sentiment_analysis(comment) -> str:
    if not comment:
        return "Empty"

    try:
        # Use older OpenAI API format
        completion = client.chat.completions.create(model="moonshotai/Kimi-K2-Instruct",
        messages=[
            {
                "role": "system",
                "content": """You are a sentiment analysis model. Classify this comment into Positive, Negative, or Neutral.
                You are to respond with one word from the option specified above. Do not provide any explanation or additional text.
                Here is the comment:
                {comment}
                """
            }
        ])
        sentiment = completion.choices[0].message.content
        return sentiment.strip()
    except Exception as e:
        print(f"Error during sentiment analysis: {e}")
        return "Error in analysis"




def start_streaming(spark):
    topic = "customers_review"
    while True:
        try:
            stream_df = spark.readStream.format("socket") \
                .option("host", "spark-master") \
                .option("port", 9999) \
                .load()

            schema = StructType([
                StructField("review_id", StringType()),
                StructField("user_id", StringType()),
                StructField("business_id", StringType()),
                StructField("stars", FloatType()),
                StructField("date", StringType()),
                StructField("text", StringType())
            ])

            stream_df = stream_df.select(from_json(col("value"), schema).alias("data")).select("data.*")

            # Register UDF for sentiment analysis
            sentiment_analysis_udf = udf(sentiment_analysis, StringType())
            
            stream_df = stream_df.withColumn("feedback", when(col('text').isNotNull(), sentiment_analysis_udf(col('text'))).otherwise("No Comment"))

            kafka_df = stream_df.selectExpr("CAST(review_id AS STRING) AS KEY", "to_json(struct(*)) AS value")

            query = (kafka_df.writeStream
                   .format("kafka")
                   .option("kafka.bootstrap.servers", config['kafka']['bootstrap.servers'])
                .option("kafka.security.protocol", config['kafka']['security.protocol'])
                .option("kafka.sasl.mechanism", config['kafka']['sasl.mechanism'])  
                .option("kafka.sasl.jaas.config",
                    f'org.apache.kafka.common.security.plain.PlainLoginModule required '
                    f'username="{config["kafka"]["sasl.username"]}" '
                    f'password="{config["kafka"]["sasl.password"]}";')
                   .option('checkpointLocation', '/tmp/checkpoint12')
                   .option('topic', topic)
                   .start()
                   .awaitTermination()
                )

            # writing to console / terminal
            # query = stream_df.writeStream.outputMode("append").format("console").options(truncate=False).start()
            # query.awaitTermination()
        except Exception as e:
            print(f'Exception encountered: {e}. Retrying in 10 seconds...')
            sleep(10)


if __name__ == "__main__":
    spark_conn = SparkSession.builder \
        .appName("SocketStreamConsumer") \
        .master("local[*]") \
        .config("spark.jars.packages",
                "org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.0") \
        .config("spark.driver.memory", "1g") \
        .config("spark.executor.memory", "1g") \
        .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoint1") \
        .getOrCreate()
    start_streaming(spark_conn)
