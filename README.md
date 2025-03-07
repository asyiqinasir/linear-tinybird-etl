# Linear to Tinybird: Initial ETL and Webhook for Updates
🔵 Linear : https://linear.app/
🐦 Tinybird : https://tinybird.co/

## Overview

This project performs an initial ETL process to seed Tinybird with data from Linear. Once the initial data is loaded, a webhook is set up to handle real-time updates, ensuring Tinybird stays in sync with Linear.

## Introduction

This project provides two main functionalities:
1. **ETL Process**: Extracts historical data from Linear API and loads it into Tinybird.
2. **Webhook Handler**: Receives real-time data updates from Linear via webhooks and sends them to Tinybird.

## Project Structure

```README.md
linear-tinybird/
├── src/
│   ├── app/
│   │   └── main.py        # Webhook handler (FastAPI app)
│   ├── etl/
│   │   └── main.py        # ETL script for historical data
│   └── utils/
│       ├── config_query.py  # Schemas and GraphQL queries
│       └── helper.py        # Utility functions
├── vercel.json            # Vercel deployment configuration
└── requirements.txt       # Project dependencies
```

## Setup

### Prerequisites

- Python 3.8+
- Linear account with API access
- Tinybird account

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/linear-tinybird-etl.git
   cd linear-tinybird-etl
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory. Refer to `.env.example` for the required variables.

## Usage

### Step 1: Running the ETL Process to populate data in Tinybird

To extract data from Linear and load it into Tinybird:

```bash
cd src
python etl/main.py Linear_Issue  # Extract issues
python etl/main.py Linear_Project  # Extract projects
python etl/main.py Linear_User  # Extract users
```

By default, the ETL process will extract all data from Linear. 
You can limit the number of records with the `--limit` flag:

```bash
python etl/main.py Linear_Issue --limit 100
```
Once the ETL process is complete, you can check the datasource in Tinybird.

## Tinybird Integration

The data is sent to Tinybird with the following datasource naming convention:
- `Linear_Issue` for issues
- `Linear_Project` for projects
- `Linear_User` for users

You can create pipes in Tinybird to analyze this data and build dashboards.

Done!

Now, we can set up the webhook to handle real-time updates from Linear.

### Step 2: Setting Up the Webhook via Vercel to stream real-time data updates to Tinybird.

The webhook handler is designed to be deployed on Vercel. The `vercel.json` file configures the deployment to use the FastAPI application in `src/app/main.py`.

1. Ensure the vercel.json is set up correctly.

2. Important: Set the environment variables in your Vercel project settings > Environment Variables.
```
1. LINEAR_WEBHOOK_SECRET=
2. TINYBIRD_API_KEY=
3. TINYBIRD_REGION=
```

3. Deploy the webhook handler to Vercel:
   ```bash
   vercel
   ```
   This will deploy the webhook handler to Vercel and provide you the deployed app url.

4. Copy the url. Optionally, you can get the url by opening Vercel and clicking on the deployed app.
    E.g: `https://your-app.vercel.app/webhook`
    
    Remember to include the `/webhook` path!

5. Configure your Linear webhook:
   - Go to Linear workspace settings
   - Navigate to Settings > API
   - Create a new webhook with your Vercel URL: `https://your-app.vercel.app/webhook`
   - Set the webhook secret. (must match LINEAR_WEBHOOK_SECRET in your Vercel app environment variables)
   - Tick to select the events you want to receive (Issues, Projects, etc.)

6. Test the webhook by creating or updating an issue in Linear.

7. Done! Open Tinybird and you should see the data being streamed in.

## Local testing: Setting up the webhook locally

To run the webhook handler locally:

```bash
cd src
uvicorn app.main:app --reload
```
You can use a tool like ngrok to expose your local server to the internet for webhook testing. 

Note: It wont work if you dont expose the local server to the internet, since webhooks require a publicly accessible url to deliver the payload. Without exposing the local server to the internet, Linear cannot send webhook events to it.

## Extra Notes

### Webhook Handler

The webhook handler is implemented using FastAPI and verifies Linear's HMAC signatures to ensure authenticity.

### How Linear's webhook authentication works
Linear use HMAC signatures rather than sending the secret directly in the headers. This is a more secure approach since the actual secret is never transmitted over the network.

Steps:
1. Implemented proper signature verification using HMAC SHA-256
2. Used the raw request body to calculate the signature
3. Compared it with the signature Linear sent in the Linear-Signature header

This approach ensures that:
1. The webhook is genuinely from Linear
2. The payload hasn't been tampered with during transmission

Future enhancement considerations:
1. Adding more detailed logging for different event types
2. Implementing error handling for malformed payloads
3. Adding a timeout mechanism for webhook processing

