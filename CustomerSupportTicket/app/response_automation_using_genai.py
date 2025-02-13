import pandas as pd
df = pd.read_csv('helpdesk_customer_multi_lang_tickets.csv')
df.head()
from pinecone import Pinecone
from pinecone import ServerlessSpec

pc = Pinecone(api_key="pcsk_7QAmeq_7L4N6t6t62BqqoVPk2WZp9sFTAoKNpNXi3V2yVkJWk3uR3cXN3HfzZx3hWwaba2")

# Instead of creating a new index, try connecting to the existing "example-index" or
# choose a different name if you intend to create a new one.
# For example, to connect to the existing "example-index":
index = pc.Index("support-tickets")

# If you want to create a new index with a different name, change "example-index" to a unique name
# pc.create_index(
#   name="new-unique-index-name",  # Changed to a new name
#   dimension=1536,
#   metric="cosine",
#   spec=ServerlessSpec(
#     cloud="aws",
#     region="us-east-1"
#   )
# )
# index = pc.Index("new-unique-index-name") # Connect to the newly created index
# index.upsert(
#     vectors=[
#         {
#             "id": "vec1", 
#             "values": [1.0, 1.5], 
#             "metadata": {"genre": "drama"}
#         }, {
#             "id": "vec2", 
#             "values": [2.0, 1.0], 
#             "metadata": {"genre": "action"}
#         }, {
#             "id": "vec3", 
#             "values": [0.1, 0.3], 
#             "metadata": {"genre": "drama"}
#         }, {
#             "id": "vec4", 
#             "values": [1.0, -2.5], 
#             "metadata": {"genre": "action"}
#         }
#     ],
#     namespace= "ns1"
# )

import google.generativeai as genai

genai.configure(api_key="AIzaSyCfMhjWIAnVNdJwamWWhP0BTTi-Y8w0H2k")
model = genai.GenerativeModel("gemini-pro")


import json
import re

def extract_issue_product(title, body):
    """
    Extract product name and issue sentence using Gemini API.
    """
    prompt = f"""Extract the product name and issue from the following:
    Title: {title}
    Body: {body}
    Provide output in JSON format with keys 'product_name' and 'issue_sentence'.
    Example body response:
    "Hello,\n\n"
        "We received your report of a network outage affecting your enterprise network involving Cisco Router ISR4331.\n"
        "Unfortunately, we were unable to find any similar issues in our knowledge base.\n"
        "We recommend that you try the following troubleshooting steps:\n"
        "1. Check the physical connections of the router and ensure that all cables are securely connected.\n"
        "2. Verify the configuration of the router and ensure that it is correct.\n"
        "3. Reboot the router and see if the issue persists.\n"
        "If you continue to experience issues, please provide us with the following information:\n"
        "1. The exact error message or symptoms you are experiencing.\n"
        "2. The configuration of the router.\n"
        "3. Any recent changes that were made to the network.\n"
        "We will be happy to assist you further once we have this information.\n"
        "Thank you,\n"
        "The Support Team"

    Follow this email template provided in the example

    If the escalation_required is True, then generate a drafted mail like this 
        Dear [Customer Name],

    Thank you for reaching out to us regarding the issue you are experiencing with [Briefly Describe the Issue, e.g., "network outage involving Cisco Router ISR4331"].

    After reviewing your case, we have determined that this issue requires further investigation by our specialized team. As a result, your case has been escalated to our Technical Escalation Team for priority handling.
    Next Steps:

        Our team will conduct an in-depth analysis of the issue.

        We will provide you with an update within [Insert Timeframe, e.g., "24-48 hours"].

        If additional information is required, we will reach out to you promptly.

    What You Can Do:

        Please ensure that you are available for further communication in case our team needs additional details.

        If you have any new information or updates regarding the issue, feel free to reply to this email.

    We understand the importance of resolving this issue quickly and are committed to providing you with a solution as soon as possible.

    Thank you for your patience and understanding.

    Best regards,
    [Your Name]
    [Your Job Title]
    [Company Name]
    [Contact Information]
    """

    response = model.generate_content(prompt)
    extracted_data = response.text.strip()

    # Remove code block markers like ```JSON and ```
    cleaned_data = re.sub(r"```[a-zA-Z]*\n|\n```", "", extracted_data).strip()

    try:
        extracted_json = json.loads(cleaned_data)
        return extracted_json.get('product_name', 'Unknown'), extracted_json.get('issue_sentence', 'Unknown')
    except json.JSONDecodeError as e:
        raise ValueError(f"Error parsing JSON response: {e}\nResponse: {cleaned_data}")


import google.generativeai as genai

def get_top_similar_issues(issue_sentence, top_k=3):
    """
    Find top similar issues using Pinecone.
    """
    # Generate embeddings using Gemini's embedding API
    embedding_response = genai.embed_content(
        model="models/embedding-001",
        content=issue_sentence,
        task_type="retrieval_document"
    )

    # Check if the response contains an embedding
    if 'embedding' not in embedding_response:
        raise ValueError("Embedding API did not return embeddings.")

    embedding = embedding_response['embedding']

    # Connect to the correct index
    index = pc.Index("support-tickets")  # Ensure the name is correct

    # Search Pinecone index
    result = index.query(vector=embedding, top_k=top_k, include_metadata=True)

    return result.get('matches', [])


import re
import json

def generate_personalized_response(product_name, issue_sentence, similar_issues):
    """
    Generate personalized response using Gemini API.
    """
    # Ensure we have at least 3 similar issues; fill missing ones with placeholders
    while len(similar_issues) < 3:
        similar_issues.append({'metadata': {'issue': 'No similar issue found', 'response': 'No response available'}})

    prompt = f"""
    Product: {product_name}
    User Issue: {issue_sentence}

    Here are similar issues and their responses:
    1. {similar_issues[0]['metadata']['issue']} - {similar_issues[0]['metadata']['response']}
    2. {similar_issues[1]['metadata']['issue']} - {similar_issues[1]['metadata']['response']}
    3. {similar_issues[2]['metadata']['issue']} - {similar_issues[2]['metadata']['response']}

    Generate a subject and a body to respond helpfully to the user.
    Provide output in JSON format with keys 'subject' and 'body'.
    """
    response = model.generate_content(prompt)

    # Clean up the response string by removing the code block markers (```)
    cleaned_data = re.sub(r"```[a-zA-Z]*\n|\n```", "", response.text.strip()).strip()

    try:
        # Parse the cleaned data as JSON
        extracted_json = json.loads(cleaned_data)
        return extracted_json.get('subject', 'No subject'), extracted_json.get('body', 'No body')
    except json.JSONDecodeError as e:
        raise ValueError(f"Error parsing JSON response: {e}\nResponse: {cleaned_data}")



def automate_response(title, body):
    """
    Full automation workflow for issue resolution.
    """
    # Step 1: Extract product name and issue
    product_name, issue_sentence = extract_issue_product(title, body)

    # Step 2: Find similar issues
    similar_issues = get_top_similar_issues(issue_sentence)

    # Step 3: Generate a personalized response
    subject, response_body = generate_personalized_response(
        product_name, issue_sentence, similar_issues
    )

    return subject,response_body



title = "App crashes on startup"
body = "Whenever I open the app, it just crashes without any error message. Please help!"
# print(pc.list_indexes())


# Try to automate the response
try:
    # Get the generated subject and response body
    result,desc = automate_response(title, body)
    
    # Print the generated response and subject in the terminal
    print("Generated Response:")
    print("Subject:", result)
    print("Body:", desc)
    # print("Subject:", result['subject'])
    # print("Body:", result['response'])
except ValueError as e:
    print("Error:", e)
