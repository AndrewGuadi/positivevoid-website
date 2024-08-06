from gpt_helpers import OpenAIHelper
from datetime import datetime

def filter_user_input(text):
    with open('openai.txt', 'r', encoding='utf-8') as file:
        api_key = file.read()
    
    intent_message = "We are moderators and processors of data. We will filter out all nonsense and foul-intended data." 

    bot = OpenAIHelper(api_key, intent_message)

    # Ask the GPT model to filter the data and tag it with necessary data.
    prompt = "You will assess the tone, meaning, and nuances of the following text and return data in the required JSON format. You will fail foul-intentioned inputs"
    example = "{'status': pass_or_fail, 'status_reason':'only_if_failed_reason_why_failed', 'text': *input_text_goes_here*, 'emotions': [array of emotions perceived in text], 'sentiment_basic': positive_neutral_negative, 'sentiment_score': on_scale_from_-100_to_+100, 'TLDR': point_of_message, 'keywords': [array of 3-10 keywords here], 'challenging_thought':'this_should_be_a_positive_stoic_spin_on_the_input_encouraging_the_user'}"

    response = bot.gpt_json(prompt, text, example)

    # Adding timestamp to the response
    current_time = datetime.now()
    timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
    response['time_stamp'] = timestamp

    return response

if __name__ == "__main__":
    text_input = input("INPUT:  ")
    response = filter_user_input(text_input)
    print(response)
