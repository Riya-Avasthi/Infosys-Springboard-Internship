import os
import json
import google.generativeai as genai
import time
import logging

logging.basicConfig(level=logging.DEBUG)

def analyze_sentiment(ticket_title, conversation_history):
    # Set API key for Google Generative AI
    genai.configure(api_key="AIzaSyCfMhjWIAnVNdJwamWWhP0BTTi-Y8w0H2k")
    model = genai.GenerativeModel("gemini-pro")

    function_schema = {
        "name": "store_sentiment",
        "description": "Store sentiment analysis results.",
        "parameters": {
            "type": "object",
            "properties": {
                "thoughts": {
                    "type": "string",
                    "description": "Details on sentiment and reasoning."
                },
                "sentiment_type": {
                    "type": "string",
                    "description": "Sentiment classification."
                }
            },
            "required": ["thoughts", "sentiment_type"]
        }
    }

    prompt = f"""
    You are a customer support agent. Determine the sentiment of the given conversation based on the title and chat history provided below. Stick to the following schema strictly:
    {json.dumps(function_schema['parameters'], indent=3)}

    Examples:
    1.
    Customer: I have an issue with my coffee maker; it's been two weeks and I still haven't received a refund.
    Agent: I’m really sorry for the delay. Could you share your order number and the bank account details for the refund?
    Sentiment: frustrated

    2.
    Customer: I'm not satisfied with the sandwich maker, I need a full refund. Your agent didn’t assist properly.
    Agent: I apologize for the inconvenience, Lisa. Could you explain the reason for cancellation?
    Customer: I found a better offer elsewhere.
    Sentiment: negative

    3.
    Customer: Is there any way I can get free delivery?
    Agent: Unfortunately, I can't provide free delivery, but I can suggest some affordable options for you.
    Sentiment: neutral

    4.
    Customer: I appreciate the quick support, thank you so much.
    Agent: You're welcome! Glad I could assist.
    Sentiment: positive

    5.
    Customer: My order was delayed for a week; I need help tracking it.
    Agent: I apologize for the delay. Let me check the status right now.
    Sentiment: frustrated

    6.
    Customer: Thanks for your help! I’ll check out the promotions and place the order.
    Agent: You’re welcome! Let us know if you need any more assistance.
    Sentiment: positive

    7.
    Customer: I have called several times about my issue, but it remains unresolved. This is really frustrating.
    Agent: I’m so sorry for the inconvenience. I will escalate this issue immediately.
    Sentiment: frustrated

    8.
    Customer: Your service is awful! No one seems to care about my issue.
    Agent: I truly apologize for how you feel. Let me work on resolving your issue right away.
    Sentiment: frustrated

    9.
    Customer: I purchased this phone based on your suggestion, but it’s not performing as expected.
    Agent: I’m really sorry to hear that. Can you share more about the specific issues you’re facing?
    Sentiment: negative

    10.
    Customer: The delivery took much longer than expected; I’m disappointed.
    Agent: I’m sorry for the delay. We’ll work on making the delivery faster next time.
    Sentiment: negative

    11.
    Customer: How can I cancel my subscription before the next billing cycle?
    Agent: Let me walk you through the cancellation process.
    Sentiment: neutral

    Title: "{ticket_title}"
    Chat History: "{conversation_history}"
    """

    try:
        time.sleep(1)  # Prevent API rate limit issues
        response = model.generate_content(prompt)

        # Log raw response for debugging
        print(f"Raw model response: {response.text}")

        # Convert the response into JSON format
        sentiment_analysis = json.loads(response.text.strip())

        # Extract sentiment details
        thoughts = sentiment_analysis.get("thoughts", "No insights provided")
        sentiment_type = sentiment_analysis.get("sentiment_type")

        if sentiment_type not in ["positive", "negative", "neutral", "frustrated"]:
            raise ValueError("Invalid sentiment classification.")

        print(f"Analysis Thought: {thoughts}")
        return {
            "sentiment": sentiment_type,
            "thoughts": thoughts
        }

    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}. Response: {response.text}")
        return None
    except ValueError as e:
        logging.error(f"Value error: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None

# Example usage
title = "cisco router issue"
chat_history = """Dear Customer Support Team, We are experiencing a complete outage affecting our enterprise network involving Cisco Router ISR4331. This disruption is critically impacting our secure WAN connectivity across all domains, urgently requiring your immediate intervention. Due to this issue, our company has halted various essential operations, significantly affecting our services and commitments to clients. As our technical team has not been able to resolve the problem internally, we need your expert support to diagnose and rectify this issue swiftly. Please consider this a high priority and provide us with the necessary technical assistance to restore our network’s functionality. Thank you for your prompt attention."""
analyze_sentiment(title, chat_history)
