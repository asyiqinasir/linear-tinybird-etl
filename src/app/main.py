import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import hmac
import hashlib
import json
from fastapi import FastAPI, Request, HTTPException
import os
from dotenv import load_dotenv
from utils.config_query import schemas
from utils.helper import check_tinybird_datasource, create_tinybird_datasource, send_to_tinybird

load_dotenv()

LINEAR_WEBHOOK_SECRET = os.getenv("LINEAR_WEBHOOK_SECRET")

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Webhook Server is Running!"}

@app.post("/webhook")
async def webhook(request: Request):
    # Get the signature from the headers
    signature = request.headers.get("Linear-Signature")
    body = await request.body()
    
    # Compute the expected signature using your webhook secret
    expected_signature = hmac.new(
        LINEAR_WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
    
    # Verify the signature
    if not signature or signature != expected_signature:
        print("Headers received:", dict(request.headers))
        print(f"Received signature: {signature}")
        print(f"Expected signature: {expected_signature}")
        raise HTTPException(status_code=403, detail="Unauthorized webhook request")
    
    # Parse the JSON payload
    payload = await request.json()
    print("Incoming Webhook Data:", payload)
    
    # Extract event type and action
    event_type = payload.get("type")
    action = payload.get("action")
    
    if event_type and action:
        # Process the webhook based on event type and action
        await process_webhook(event_type, action, payload)
    
    return {"status": "success"}

async def process_webhook(event_type, action, payload):
    """Process webhook data based on event type and action"""
    tinybird_event_name = f"Linear_{event_type}"
    schema = schemas.get(tinybird_event_name)
    
    print(f"Processing event: {event_type} - {action}")
    
    # Check if we need to create the datasource
    if not check_tinybird_datasource(tinybird_event_name):
        if schema:
            create_tinybird_datasource(tinybird_event_name, schema)
        else:
            print(f"No schema defined for {tinybird_event_name}")
            return
    
    # Process data based on event type
    if event_type == "Issue":
        await handle_event_issue(action, payload, tinybird_event_name, schema)
    elif event_type == "Project":
        await handle_event_project(action, payload, tinybird_event_name, schema)
    elif event_type == "User":
        await handle_event_user(action, payload, tinybird_event_name, schema)
    else:
        print(f"Unhandled event type: '{event_type}'. Please update codebase to handle this event type.")

async def handle_event_issue(action, payload, event_name, schema):
    issue = payload.get("data", {})
    print(f"Webhook App - Received Issue {action} - id: {issue.get('id')}, Title: {issue.get('title')}")
    send_to_tinybird([issue], event_name, schema)

async def handle_event_project(action, payload, event_name, schema):
    project = payload.get("data", {})
    print(f"Webhook App - Received Project {action} - id: {project.get('id')}, Name: {project.get('name')}")
    send_to_tinybird([project], event_name, schema)

async def handle_event_user(action, payload, event_name, schema):
    user = payload.get("data", {})
    print(f"Webhook App - Received User {action} - id: {user.get('id')}, Name: {user.get('name')}")
    send_to_tinybird([user], event_name, schema)