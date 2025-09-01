config = {
    "openai": {
        "api_key": "huggingface_api_key"
    },
    "kafka": {
        "sasl.username": "confluent_cloud_key",
        "sasl.password": "confluent_cloud_password",
        "bootstrap.servers": "pkc-yourcode.us-central1.gcp.confluent.cloud:9092",
        "security.protocol": "SASL_SSL",
        "sasl.mechanism": "PLAIN",
        "session.timeout.ms": 50000
    },
    "schema_registry": {
        "url": "https://yourcode.us-central1.gcp.confluent.cloud",
        "basic.auth.user.info": "key:secret"
    }
}