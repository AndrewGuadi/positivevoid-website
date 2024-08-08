from datetime import datetime
from models import ProcessedThought
from app import app, db
from gpt_helpers import OpenAIHelper  # Adjust this import as necessary
import re
import json

def get_api_key():
    try:
        variable = open('openai.txt', 'r', encoding='utf-8').read().strip()
    except Exception as e:
        print("Unable to read API KEY:", e)
        variable = None
    return variable

def get_thoughts():
    with app.app_context():
        try:
            data = ProcessedThought.query.all()
        except Exception as e:
            print("Unable to retrieve thoughts:", e)
            data = []
        return data

def is_today(date_string):
    """
    Checks if the given date_string is from today.
    Assumes date_string is in the format '%Y-%m-%d %H:%M:%S'.
    """
    thought_date = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S').date()
    today = datetime.now().date()
    return thought_date == today

def get_todays_thoughts():
    """
    Returns a list of ProcessedThoughts from today.
    """
    thoughts = get_thoughts()
    todays_thoughts = [thought for thought in thoughts if is_today(thought.time_stamp)]
    return todays_thoughts

def preprocess_text(text):
    """
    Cleans the text data by removing extra spaces and trimming.
    """
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def aggregate_thoughts(thoughts):
    """
    Aggregates the thoughts using GPT and returns a comprehensive analysis.
    """
    api_key = get_api_key()
    intent_message = "You are to analyze and summarize the day's thoughts."
    helper = OpenAIHelper(api_key, intent_message)

    cleaned_thoughts = [preprocess_text(thought.original_text) for thought in thoughts]
    data = "\n".join(cleaned_thoughts)

    prompt = """
    You will analyze the following thoughts recorded throughout the day. Your tasks are:
    1. Provide a generalized assessment of the day.
    2. Return the most associated keywords for the day.
    3. Generate a quote that captures the total sentiment of the day.
    4. Provide a sentiment gauge:
        a. Simple gauge ranging from negative to neutral to positive.
        b. Detailed gauge ranging on a scale from -100 to +100.
    5. Identify any other interesting insights or JSON keys that could be useful.

    Here are the thoughts:
    """
    example = {
        "general_assessment": "Assess all the data and give your assessment",
        "keywords": ['return a list of keywords'],
        "quote": "refer to a real quote here",
        "sentiment_gauge_simple": "positive_neutral_or_negative",
        "sentiment_gauge_detailed": "float value to capture detailed sentiment from -100(most negative) to +100(most positive)",
        "additional_insights": {"most_frequent_emotion": "indenitfy most frequent emotions", "average_sentiment_score": 'float between -100 and +100'}
    }

    response = helper.gpt_json(prompt, data, json.dumps(example))
    return response

if __name__ == "__main__":
    thoughts = get_todays_thoughts()
    response = aggregate_thoughts(thoughts)
    
    # Extract and display the results
    general_assessment = response.get("general_assessment")
    keywords = response.get("keywords")
    quote = response.get("quote")
    sentiment_gauge_simple = response.get("sentiment_gauge_simple")
    sentiment_gauge_detailed = response.get("sentiment_gauge_detailed")
    additional_insights = response.get("additional_insights")
    
    print("General Assessment:", general_assessment)
    print("Keywords:", keywords)
    print("Quote:", quote)
    print("Simple Sentiment Gauge:", sentiment_gauge_simple)
    print("Detailed Sentiment Gauge:", sentiment_gauge_detailed)
    print("Additional Insights:", additional_insights)




