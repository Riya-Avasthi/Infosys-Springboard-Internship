import os
import json
import google.generativeai as genai
import time
import logging

logging.basicConfig(level=logging.DEBUG)

def get_sentiment(title, chat_history):
    genai.configure(api_key="AIzaSyCfMhjWIAnVNdJwamWWhP0BTTi-Y8w0H2k")
    model = genai.GenerativeModel("gemini-pro")

    function_schema = {
        "name": "save_sentiment",
        "description": "Save sentiment related data.",
        "parameters": {
            "type": "object",
            "properties": {
                "thought": {
                    "type": "string",
                    "description": "Your thoughts on sentence and sentiment"
                },
                "sentiment": {
                    "type": "string",
                    "description": ""
                }
            },
            "required": ["thought", "sentiment"]
        }
    }

    prompt = f"""
    You are a Support Agent. You have to decide on sentiment of the given ticket for which you are given:
    1. Title
    2. Chat History

    Follow this JSON schema strictly:
    {json.dumps(function_schema['parameters'], indent=3)}

    Examples:
    1.
    ...
    Customer: Hi, I returned a coffee maker two weeks ago, and I haven't received the refund in my bank account yet.
    Agent: I'm sorry to hear that. Can you please provide me with your order number and the bank account details that you provided for the refund?
    ...
    Sentiment: frustrated

    2.
    ...
    Customer: Hi Tom, I want a full refund for my sandwich maker. Your agent is not helping me.
    Agent: I'm sorry to hear that, Lisa. May I know the reason for the cancellation?
    Customer: I found a better deal on another website.
    ...
    Sentiment: negative

    3.
    ...
    Customer: Oh, I see. I wasn't aware of that. Is there anything I can do to get free delivery?
    Agent: I'm afraid not, but I can suggest a few options that might help you save on delivery charges.
    ...
    Sentiment: neutral

    4.
    ...
    Customer: Thanks for the quick resolution! I really appreciate the support.
    Agent: You're welcome! We're glad we could assist you. Have a great day!
    ...
    Sentiment: positive

    5.
    ...
    Customer: I need help with tracking my order. It's been delayed for a week.
    Agent: I'm sorry for the delay. Let me check the status and provide you an update shortly.
    ...
    Sentiment: frustrated

    6.
    ...
    Customer: Thanks for your assistance. I'll check the promotions and proceed with the order.
    Agent: You're welcome! Let us know if you need any further help.
    ...
    Sentiment: positive

    7.
    ...
    # The customer repeatedly complains about an unresolved issue.
    Customer: I've called multiple times about this issue, and it's still not resolved. This is getting really frustrating.
    Agent: I sincerely apologize for the repeated inconvenience. Let me escalate this to a senior representative right away.
    ...
    Sentiment: frustrated

    8.
    ...
    # The customer expresses strong dissatisfaction with service.
    Customer: Your service is the worst I've ever experienced! No one seems to care about my issue.
    Agent: I'm really sorry you feel this way. I'll do my best to address your concerns right now.
    ...
    Sentiment: frustrated

    9.
    ...
    # The customer expresses dissatisfaction but not frustration.
    Customer: I bought this phone based on your recommendation, and it’s not as good as expected.
    Agent: I apologize for the inconvenience. Could you please share what specific issues you're facing?
    ...
    Sentiment: negative

    10.
    # The customer expresses disappointment due to an unmet expectation.
    Customer: I expected faster delivery, but it took way longer than what was promised.
    Agent: I'm sorry about the delay. We will ensure quicker delivery next time.
    ...
    Sentiment: negative

    11.
    # The customer provides factual information without strong emotions.
    Customer: I need to know how to cancel my subscription before the next billing cycle.
    Agent: Sure, I can guide you through the cancellation process.
    ...
    Sentiment: neutral

    12.
    # The conversation remains informative without positive or negative tones.
    Customer: Can you please confirm if the product is available in my region?
    Agent: Let me check that for you. Could you provide your ZIP code?
    ...
    Sentiment: neutral

    13.
    # The customer expresses mild appreciation.
    Customer: The support team was helpful. Thanks for the assistance.
    Agent: Glad to hear that! Let us know if you need anything else.
    ...
    Sentiment: positive

    14.
    # The customer shows strong enthusiasm.
    Customer: I love the new update! It's exactly what I wanted.
    Agent: Thank you for your feedback! We're glad you like it.
    ...
    Sentiment: positive

    15.
    # The customer is delighted with the resolution.
    Customer: Wow! That was super fast. I really appreciate the support.
    Agent: Thank you for your kind words! We're always happy to help.
    ...
    Sentiment: positive

    16.
    # The customer feels unheard and expresses concern about communication.
    Customer: I've sent multiple emails, and no one has responded to me yet.
    Agent: I'm really sorry about that. I'll personally follow up on your request now.
    ...
    Sentiment: frustrated

    17.
    # The customer is just asking about product details without emotion.
    Customer: Does this laptop support 4K resolution?
    Agent: Yes, it supports up to 4K UHD resolution with HDR.
    ...
    Sentiment: neutral

    18.
    ...
    # The customer expresses dissatisfaction but is open to solutions.
    Customer: The software keeps crashing. I hope there's a fix for this soon.
    Agent: I'm sorry to hear that. Let me check for any available updates or troubleshooting steps.
    ...
    Sentiment: negative

    19.
    ...
    # The customer expresses gratitude after a long-standing issue is resolved.
    Customer: Finally! The issue is fixed. Thanks a ton for your patience and support.
    Agent: We're happy to help! Let us know if you need anything else.
    ...
    Sentiment: positive

    20.
    ...
    # The customer reports an issue but remains patient.
    Customer: My internet speed has been slow lately, but I understand these things happen.
    Agent: Thanks for your understanding. Let me check if there are any network issues in your area.
    ...
    Sentiment: neutral

    21.
    ...
    # The customer is angry about being misled by previous information.
    Customer: Your team told me I'd get a replacement in 3 days, but it’s been over a week!
    Agent: I sincerely apologize for the miscommunication. Let me check on your replacement order immediately.
    ...
    Sentiment: frustrated

    22.
    ...
    # The customer provides feedback in a constructive manner.
    Customer: The product works fine, but I think it could use some improvements in battery life.
    Agent: Thanks for your feedback! We'll pass it along to our development team.
    ...
    Sentiment: neutral

    23.
    ...
    # The customer is expressing mild concern about repeated issues.
    Customer: I've been facing the same problem again. Is there a permanent solution to this?
    Agent: I apologize for the recurring issue. I'll escalate this to our technical team for a thorough check.
    ...
    Sentiment: frustrated

    24.
    ...
    # The customer asks a generic question without showing emotion.
    Customer: Can you tell me your store's operating hours?
    Agent: Sure! Our store is open from 9 AM to 9 PM daily.
    ...
    Sentiment: neutral

    25.
    ...
    # The customer shows slight annoyance but remains polite.
    Customer: I was hoping to get a quicker response, but I understand you must be busy.
    Agent: Thanks for your patience! How can I assist you today?
    ...
    Sentiment: neutral

    26.
    ...
    # The customer demands a solution aggressively.
    Customer: I need this fixed RIGHT NOW! This delay is unacceptable.
    Agent: I understand your frustration. Let me prioritize your request immediately.
    ...
    Sentiment: frustrated

    27.
    ...
    # The customer expresses appreciation without strong excitement.
    Customer: Thanks, this information was helpful.
    Agent: Glad to be of assistance! Let us know if you need more help.
    ...
    Sentiment: positive

    28.
    ...
    # The customer expresses happiness after using the product.
    Customer: I must say, this is one of the best purchases I've made!
    Agent: That's wonderful to hear! Thank you for your feedback.
    ...
    Sentiment: positive

    29.
    ...
    #anything regarding refund requests are frustrating
    customer: i request a refund for the product
    Agent: I understand your frustration. Let me prioritize your request immediately.
    ...
    Sentiment: frustrated

    Title: "{title}"
    Chat History: "{chat_history}"
    """

    try:
        time.sleep(1)  # To avoid API rate limits
        response = model.generate_content(prompt)

        # Log raw response for debugging
        # print(f"Raw response from model: {response.text}")

        # Parse the response into JSON
        sentiment_data = json.loads(response.text.strip())

        # Extract and validate sentiment
        thought = sentiment_data.get("thought", "No thought provided")
        sentiment = sentiment_data.get("sentiment")

        if sentiment not in ["positive", "negative", "neutral", "frustrated"]:
            raise ValueError("Invalid sentiment value returned by the model.")

        # print(f"Model's Thought: {thought}")
        return {
            "sentiment" : sentiment,
            "thought" : thought
        }

    except json.JSONDecodeError as e:
        logging.error(f"JSON decoding error: {e}. Response: {response.text}")
        return None
    except ValueError as e:
        logging.error(f"Value error: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None
    
title = "cisco router issue"
chat_history = """Dear Customer Support Team, We are experiencing a complete outage affecting our enterprise network involving Cisco Router ISR4331. This disruption is critically impacting our secure WAN connectivity across all domains, urgently requiring your immediate intervention. Due to this issue, our company has halted various essential operations, significantly affecting our services and commitments to clients. As our technical team has not been able to resolve the problem internally, we need your expert support to diagnose and rectify this issue swiftly. Please consider this a high priority and provide us with the necessary technical assistance to restore our network’s functionality. Thank you for your prompt attention."""
result  = get_sentiment(title, chat_history)
print(f"Sentiment: {result['sentiment']}")
print(f"Thought: {result['thought']}")

