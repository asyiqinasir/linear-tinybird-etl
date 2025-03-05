import requests
import json
import logging
import os
from dotenv import load_dotenv

load_dotenv()

LINEAR_API_KEY = os.getenv("LINEAR_API_KEY")
TINYBIRD_API_KEY = os.getenv("TINYBIRD_API_KEY")
TINYBIRD_REGION = os.getenv("TINYBIRD_REGION", "us-east")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def fetch_linear_data(graphql_query):
    linear_url = "https://api.linear.app/graphql"
    headers = {
        "Authorization": f"{LINEAR_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(linear_url, headers=headers, json={"query": graphql_query})

        if response.status_code != 200:
            logging.error(f"Linear - HTTP {response.status_code} - Failed request to Linear API")
            logging.error(f"Linear - Response Text: {response.text}")
            return None

        response_data = response.json()

        if "errors" in response_data:
            logging.error(f"Linear - {response_data['errors']}")
            return None

        root_key = list(response_data["data"].keys())[0]  # E.g., "projects" or "issues"
        records = response_data.get("data", {}).get(root_key, {}).get("nodes", [])

        if not records:
            logging.warning("Linear - No data retrieved from Linear API.")
            return None
        logging.info(f"Linear - Successfully fetched {len(records)} records.")
        return records

    except requests.exceptions.RequestException as e:
        logging.error(f"Linear - HTTP Request Error: {e}")
        return None


def send_to_tinybird(data, event_name, schema=None):
    tinybird_url = f"https://api.{TINYBIRD_REGION}.tinybird.co/v0/events?name={event_name}"

    headers = {
        "Authorization": f"Bearer {TINYBIRD_API_KEY}",
        "Content-Type": "application/json"
    }

    tinybird_payload = "\n".join(json.dumps(record) for record in data)

    params = {}
    if schema:
        params["schema"] = schema

    try:
        response = requests.post(tinybird_url, headers=headers, data=tinybird_payload, params=params)
        response_json = response.json()

        if response.status_code == 202:
            logging.info(f"Tinybird - Data successfully sent to data source: {event_name}")
            logging.info(f"Tinybird - {response_json['successful_rows']} rows ingested, {response_json['quarantined_rows']} quarantined.")
            return True
        elif response.status_code != 200:
            logging.error(f"Tinybird - HTTP {response.status_code} - Failed request to Tinybird")
            logging.error(f"Tinybird -Response Text: {response.text}")
            return False
        return True

    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending data to Tinybird: {e}")
        return False