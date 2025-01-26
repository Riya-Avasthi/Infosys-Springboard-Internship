from fastapi import FastAPI, HTTPException
import requests
import json

app = FastAPI()

# Zapier Webhook URL (Replace with your actual Zapier webhook URL)
ZAPIER_WEBHOOK_URL = "https://hooks.zapier.com/hooks/catch/21362029/2f2c57n/"

@app.post("/send-zapier-webhook")
async def send_zapier_webhook(
    email: str,
    subject: str,
    body: str
):
    """
    Endpoint to send a webhook payload to Zapier for email integration.
    """
    # Build the payload to send to Zapier
    payload = {
        "email": email,
        "subject": subject,
        "body": body
    }

    try:
        # Send the POST request to Zapier
        response = requests.post(ZAPIER_WEBHOOK_URL, json=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            return {"status": "success", "details": "Email sent via Zapier"}
        else:
            return HTTPException(
                status_code=response.status_code,
                detail=f"Zapier webhook failed: {response.text}"
            )
    except Exception as e:
        # Handle any exceptions
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

