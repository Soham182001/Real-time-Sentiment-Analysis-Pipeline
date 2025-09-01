from huggingface_hub import InferenceClient
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import config


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
        print(sentiment)
        return sentiment.strip()
    except Exception as e:
        print(f"Error during sentiment analysis: {e}")
        return "Error in analysis"

if __name__ == "__main__":
    # Test with a sample comment
    test_text = "First time there and it was excellent!!! It feels like your are entering someone's home. The waiters there funny and nice. The food come out very quickly and it is phenomenal!!! Definitely will be going back to this place."
    result = sentiment_analysis(test_text)
    print(f"Input: {test_text}")
    print(f"Sentiment: {result}")