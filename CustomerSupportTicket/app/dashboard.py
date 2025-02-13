### For practice
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import nltk
from textblob import TextBlob
from pymongo import MongoClient # for database connectivity
from datetime import datetime
from response_automation_using_genai import automate_response
from issue_escalation import escalateit
from sentiment_analysis_using_gemini import get_sentiment
import json
# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
import requests

# Function to send data to Zapier Webhook
def send_to_zapier_webhook(title, body, response):
    ZAPIER_WEBHOOK_URL = "https://hooks.zapier.com/hooks/catch/21651217/2alrmst/"  # Replace with your Zapier webhook URL
    
    payload = {
        "to" : "riya04avasthi@gmail.com",
        "title": title,
        "body": body,
        "response": response,
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(ZAPIER_WEBHOOK_URL, json=payload)

        if response.status_code == 200:
            return "Email sent successfully via Zapier webhook!"
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Zapier webhook failed: {response.text}"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


#function for storing data
def store_data_in_mongodb(title, body, sentiment=None, escalation=None, response=None):
    # Connect to MongoDB (make sure MongoDB is running locally or remotely)
    client = MongoClient("mongodb://localhost:27017")  # Replace with your MongoDB connection string
    db = client["customer_tickets"]  # Database name
    collection = db["tickets"]  # Collection name based on data type (sentiment, escalation, response)

   # Create a data document with the required structure
    data_document = {
        "title": title,
        "body": body,
        "timestamp": datetime.utcnow().isoformat(),  # Format timestamp as ISO 8601
        "sentiment": sentiment,
        "escalation": escalation,
        "response": response
    }

    # Insert the document into the MongoDB collection
    result = collection.insert_one(data_document)

    return result.inserted_id


def generate_automated_response(title, body):
    sentiment = get_sentiment(title, body)
    priority = escalateit(title, body)
    
    # More contextual responses
    responses = {
        "Very Positive": "Thank you for your wonderful feedback! We're thrilled to hear about your positive experience.",
        "Slightly Positive": "Thank you for your feedback! We're glad to hear about your experience.",
        "Neutral": "Thank you for reaching out. We'll review your message and get back to you soon.",
        "Slightly Negative": "We apologize for any inconvenience you've experienced. Our team will look into this matter.",
        "Very Negative": "We sincerely apologize for your negative experience. This will be escalated to our team immediately for urgent attention."
    }
    
    # Select the appropriate response based on sentiment
    response = responses.get(sentiment['sentiment'], responses["Neutral"])
    response_subject, response_body = automate_response(title, body)

    # Add priority-based additional message
    if priority != False:
        response += f"\n\nThis has been marked as priority and needs to be escalated and will be handled accordingly."

    # Combine the subject, body, and response into one plain text variable
    combined_response = f"{response_subject}\n\n{response_body}\n\n{response}"

    # Store data in MongoDB
    store_data_in_mongodb(title, body, sentiment=sentiment['sentiment'], escalation=priority, response=combined_response)
    
    return combined_response


def main():
    st.set_page_config(page_title="Issue Analysis Tool", layout="wide")
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stTextInput > div > div > input {
            padding: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Sidebar Navigation
    with st.sidebar:
        st.title("Navigation")
        selected = option_menu(
            menu_title=None,
            options=["Sentiment Analysis", "Issue Escalation", "Automated Response"],
            icons=["emoji-smile", "arrow-up-circle", "chat-dots"],
            menu_icon="cast",
            default_index=0,
        )
        
        # Add some information in sidebar
        st.markdown("---")
        st.markdown("### About")
        st.info("""
        This tool helps analyze customer issues by:
        - Determining sentiment
        - Predicting escalation needs
        - Generating automated responses
        """)
    
    if selected == "Sentiment Analysis":
        st.header("Sentiment Analysis")
        
        # Create top-level buttons above inputs
        col1, col2 = st.columns(2)
        with col1:
            run_analysis = st.button("Run Analysis", type="primary", use_container_width=True)
        with col2:
            view_pipeline = st.button("View Pipeline", use_container_width=True)
        
        st.markdown("---")  # Add separator
        
        # Input fields
        title = st.text_input("Issue Title", value="Payment Processing Failure – Transactions Declined")
        body = st.text_area("Issue Body", value="Unable to complete their purchases due to a sudden payment gateway failure. Multiple transactions are getting declined without any error messages.", height=200)
        
        if run_analysis:
            if title or body:
                result = get_sentiment(title, body)
                sentiment = result['sentiment']
                explanation = result['thought']
                emoji = ""

                # Assign emoji based on sentiment
                if sentiment == "positive":
                    emoji = "😊"  # Happy emoji for positive sentiment
                elif sentiment == "negative":
                    emoji = "😡"  # Angry emoji for negative sentiment
                elif sentiment == "neutral":
                    emoji = "😐"  # Neutral emoji for neutral sentiment
                elif sentiment == "frustrated":
                    emoji = "😤"  # Frustrated emoji for frustrated sentiment
                
                # Display sentiment with emoji
                # col1, col2, col3 = st.columns(3)
                # with col1:
                st.metric("Sentiment", f"{emoji}{sentiment}")
                st.text_area("Explanation", explanation)
                # Enhanced visualization
                # st.subheader("Sentiment Visualization")
                # fig_col1, fig_col2 = st.columns(2)

            else:
                st.warning("Please enter either a title or body text to analyze")
        
        if view_pipeline:
            st.subheader("Sentiment Analysis Pipeline")
            st.image("Sentiment_Analysis_pipeline.png",
                    caption="Sentiment Analysis Infrastructure",
                    width=600)
            st.markdown("""
            **Pipeline Steps:**
            1. Configure API Key – Set up authentication for Google Generative AI (genai.configure(api_key=...)).

            2. Define Model – Initialize gemini-pro model.

            3. Define Function Schema – Create a JSON schema that enforces a structured output format.

            4. Construct Prompt – Format the prompt with:
                Title
                Chat History
                Example cases covering different sentiment categories.
                        
            5. API Call – Call model.generate_content(prompt) to get the model’s response.

            6. Handle Response – Process the model’s output:
                Parse the response as JSON.
                Extract thought and sentiment values.
                Validate that the sentiment is one of: positive, negative, neutral, or frustrated.
                        
            7. Error Handling – Handle potential exceptions
                json.JSONDecodeError (if response parsing fails)
                ValueError (if an invalid sentiment is returned)
                Generic exceptions for API or unexpected errors.
            8. Return Result – Output a structured dictionary
            """)
    
    elif selected == "Issue Escalation":
        st.header("Issue Escalation Prediction")
        
        # Create top-level buttons above inputs
        col1, col2 = st.columns(2)
        with col1:
            run_prediction = st.button("Run Prediction", type="primary", use_container_width=True)
        with col2:
            view_pipeline = st.button("View Pipeline", use_container_width=True)
        
        st.markdown("---")  # Add separator
        
        # Input fields
        title = st.text_input("Issue Title", value="Payment Processing Failure – Transactions Declined")
        body = st.text_area("Issue Body", value="Unable to complete their purchases due to a sudden payment gateway failure. Multiple transactions are getting declined without any error messages.", height=200)
        
        if run_prediction:
            if title or body:
                escalated = escalateit(title, body)
                
                if escalated == True:
                    #st.text_area("🚨Issue needs to be escalted !!")
                    st.markdown(
                        """
                        <div style="
                            background-color:#f74856;
                            color:#f2e1e3;
                            padding:10px;
                            border-radius:5px;
                            font-size:16px;
                            font-weight:bold;
                            text-align:center;
                        ">
                            🚨 Issue needs to be escalated !!
                        </div>
                        """,
                        unsafe_allow_html=True,
    
                    )
                    #st.warning("🚨Issue needs to be escalted !!")

                else:
                    st.success("✓ Normal Priority Issue, No escalation Needed !!")
                
                st.subheader("Analysis Details")
                st.write("**Escaltion Level:**", escalated)

            else:
                st.warning("Please enter either a title or body text to analyze")
        
        if view_pipeline:
            st.subheader("Issue Escalation Pipeline")
            st.image("Issue_Escalation_Pipeline.png",
                    caption="Escalation Prediction Infrastructure",
                    width=600)
            st.markdown("""
            **Pipeline Steps:**
            1. Input Data: Gather title and description as inputs.
        
            2. Combine and Normalize: Concatenate and convert to lowercase.
                        
            3. Critical Keywords Check: Check for presence of critical keywords (e.g., "issue", "problem").
            
            4. Specific Keywords Check: Check for specific keywords (e.g., "security", "compliance").
           
            5. No Match for Escalation: Return False if no keywords are found.
            
            6. Return Final Result: Return True for escalation or False for no escalation.
            """)
    
    else :
        st.header("Automated Response Generation")
    
        # Create top-level buttons above inputs
        col1, col2 = st.columns(2)
        with col1:
            generate_response = st.button("Generate Response", type="primary", use_container_width=True)
        with col2:
            view_pipeline = st.button("View Pipeline", use_container_width=True)
    
        st.markdown("---")  # Add separator
        
        # Input fields
        title = st.text_input("Issue Title", value="Payment Processing Failure – Transactions Declined")
        body = st.text_area("Issue Body", value="Unable to complete their purchases due to a sudden payment gateway failure. Multiple transactions are getting declined without any error messages.", height=200)
        
        if generate_response:
            if title or body:
                # Generate automated response
                response = generate_automated_response(title, body)

                #changing style for text area
                st.markdown(
                    """
                    <style>
                    .stTextArea textarea {
                        background-color:rgb(248, 213, 213); /* Light blue background */
                        color:rgb(19, 18, 18); /* Dark blue text */
                        font-size: 16px;
                        font-weight: bold;
                        border-radius: 5px;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )
                st.text_area("Generated Response", response, height=400)
                 # Send to Zapier Webhook
                send_result = send_to_zapier_webhook(title, body, response)
                st.success(f"Response sent to email via Zapier: {send_result}")
                escaped_response = json.dumps(response)  # Ensures proper formatting for JavaScript

                st.markdown(f"""
                    <div style="background-color: #0a0a0a; padding: 1rem; border-radius: 0.5rem; color:#f5dada">
                        <p style="margin-bottom: 0.5rem;"><strong>Quick Actions:</strong></p>
                        <button onclick="navigator.clipboard.writeText('{escaped_response}')" style="padding: 0.5rem 1rem;">
                            Copy Response
                        </button>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("Please enter either a title or body text to generate a response")
        
        if view_pipeline:
            st.subheader("Response Generation Pipeline")
            st.image("Response_Automation_pipeline.png",
                    caption="Automated Response Infrastructure",
                    use_container_width=True)
            
            st.markdown("""
            **Pipeline Steps:**
                        
            1.Extract Product & Issue
                Use Gemini API to extract the product name and issue sentence from the title and body.
                Ensure the response is parsed as JSON.
                        
            2.Generate Embeddings for Issue Sentence
                Convert issue sentence into an embedding using Gemini's embedding API.
                        
            3.Retrieve Similar Issues
                Search for the most relevant past issues using Pinecone vector search.
                Retrieve metadata including similar issue descriptions and responses.
            
            4.Generate Personalized Response
                Use Gemini API to generate a subject and response body.
                Incorporate similar issue responses for better accuracy.
            
            5.Automate the Full Workflow
                Extract product name and issue.
                Find similar past issues.
                Generate a final, personalized response.
            
            6.Return the Response for user communication.
                        
            7.Automate Response through Mail
                        
            8.Save Data in DB
            """)
            
if __name__ == "__main__":
    main()