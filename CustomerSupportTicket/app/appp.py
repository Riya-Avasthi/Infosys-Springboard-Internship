
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models.S import analyze_sentiment
from models.R import automate_response
from models.I import escalateit
import requests
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Dict

# Initialize FastAPI app
app = FastAPI()

# Set your actual Zapier Webhook URL here
ZAPIER_WEBHOOK_URL = "https://hooks.zapier.com/hooks/catch/21362029/2f2c57n/"

# MongoDB client configuration
MONGO_URL = "mongodb://ticket:27017"  # Change this to your MongoDB URL if needed
DATABASE_NAME = "tickets_system"
COLLECTION_NAME = "tickets"

# Define the Ticket model
class Ticket(BaseModel):
    subject: str
    body: str
    customer_email: str

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# MongoDB client initialization
@app.on_event("startup")
async def startup_db():
    app.mongodb_client = AsyncIOMotorClient(MONGO_URL)
    app.db = app.mongodb_client[DATABASE_NAME]
    app.collection = app.db[COLLECTION_NAME]

@app.on_event("shutdown")
async def shutdown_db():
    app.mongodb_client.close()

@app.post("/process-ticket/")
async def process_ticket(ticket: Ticket):
    try:
        # Step 1: Sentiment analysis
        sentiment_result = analyze_sentiment(ticket.subject, ticket.body)

        # Handle different types of sentiment analysis results
        if isinstance(sentiment_result, str):
            sentiment = sentiment_result
            thought = ""  # No additional thought if it's just a string sentiment
        elif isinstance(sentiment_result, dict) and "sentiment" in sentiment_result:
            sentiment = sentiment_result["sentiment"]
            thought = sentiment_result.get("thought", "")  # Default to empty string if no thought
        else:
            raise ValueError("Invalid response from sentiment analysis model")

        # Step 2: Set priority based on sentiment
        priority = "high" if sentiment == "frustrated" else "low"

        # Step 3: Prepare issue for escalation based on certain tags (simplified example)
        incoming_issue = {
            "priority": priority,
            "tag_1": ticket.subject,
            "tag_2": ticket.body,
            "tag_3": ""
        }

        # Step 4: Determine if issue escalation is needed
        escalation_required = escalateit(incoming_issue)

        # Update priority if escalation is required
        priority = "high" if escalation_required else "low"

        # Step 5: Automate the response
        auto_response = automate_response(ticket.subject, ticket.body)

        # Construct response payload
        response = {
            "customer_email": ticket.customer_email,
            "customer_ticket": ticket.body,
            "sentiment": sentiment,
            "thought": thought,
            "escalation_required": escalation_required,
            "priority": priority,
            "response": auto_response
        }

        # Step 6: Save the response to MongoDB
        result = await app.collection.insert_one(response)  # Insert into MongoDB

        # Step 7: Prepare Zapier payload
        zapier_payload = {
            "To": ticket.customer_email,
            "Subject": f"Issue Report: {ticket.subject}",
            "Body": f"{auto_response}\nThank you for bringing this to our attention.\nRegards, Support Team"
        }

        # Step 8: Send data to Zapier via webhook
        zapier_response = requests.post(ZAPIER_WEBHOOK_URL, json=zapier_payload)
        zapier_response.raise_for_status()  # Raise error if something goes wrong

        # Return response to client
        return {"status": "success", "message": "Ticket processed successfully", "ticket_id": str(result.inserted_id)}

    except requests.RequestException as req_err:
        logging.error("Error sending data to Zapier: %s", str(req_err))
        raise HTTPException(status_code=500, detail=f"Failed to send data to Zapier: {str(req_err)}")
    except ValueError as val_err:
        logging.error("Value error: %s", str(val_err))
        raise HTTPException(status_code=400, detail=f"Processing error: {str(val_err)}")
    except Exception as e:
        logging.error("Unexpected error: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@app.get("/")
def root():
    return {"message": "Ticket Processing API is running. Use POST /process-ticket/ to process a ticket."}
