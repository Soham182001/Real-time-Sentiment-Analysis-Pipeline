# Real-time Sentiment Analysis Pipeline

## Project Description
This project implements a real-time sentiment analysis pipeline for customer reviews using Apache Spark Structured Streaming and Kafka. The system processes incoming customer reviews in real-time, performs sentiment analysis using OpenAI's GPT model, and streams the results to a Kafka topic.

## Technologies Used
- Apache Spark 4.0.0: For distributed stream processing
- Apache Kafka: Message broker for handling real-time data streams
- Python 3.x: Primary programming language
- OpenAI GPT: For sentiment analysis
- Docker: For containerization and deployment
- Confluent Cloud: Managed Kafka service
- Hugging Face: For ML model inference

## Project Structure
- streaming-socket.py: Socket server for streaming review data
- spark-streaming.py: Main Spark streaming job for processing data
- config.py: Configuration settings for Kafka and OpenAI

## Running the Application

### Prerequisites
- Docker Desktop installed
- Docker Compose installed

### Build and start containers in detached mode
docker compose up -d --build

### Verify containers are running
docker ps

### Start Spark Streaming Job
```bash
docker exec -it spark-master \
  spark-submit \
  --master spark://spark-master:7077 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.0 \
  /opt/bitnami/spark/jobs/spark-streaming.py
```

### Start Socket Stream
```bash
docker exec -it spark-master /bin/bash
python jobs/streaming-socket.py
```

## Data Flow
1. Customer reviews are ingested through a socket connection
2. Spark Structured Streaming processes the incoming data
3. Each review is analyzed for sentiment using OpenAI's GPT model
4. Results are written to a Kafka topic
5. Processed data can be consumed by downstream applications

## Requirements
- Docker and Docker Compose
- Python 3.x
- Apache Spark 4.0.0
- Confluent Cloud account
- OpenAI API key

## Configuration
Ensure all necessary credentials are properly configured in config.py:
- Kafka bootstrap servers
- SASL credentials
- OpenAI API key
- Schema Registry settings

## Dataset
Create a Dataset folder inside src
and download the dataset from https://business.yelp.com/data/resources/open-dataset/



### ps: if you dont want to run it in docker change the host to localhost in spark-streaming.py and streaming-socker.py
and simply run two python scripts individually