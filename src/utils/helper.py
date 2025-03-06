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

def check_tinybird_datasource(event_name):
    """Check if the Tinybird Data Source already exists. If it exists, ignore."""
    url = f"https://api.{TINYBIRD_REGION}.tinybird.co/v0/datasources"
    headers = {"Authorization": f"Bearer {TINYBIRD_API_KEY}"}

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        datasources = response.json().get("datasources", [])
        for ds in datasources:
            if ds["name"] == event_name:
                logging.info(f"Tinybird - Data Source '{event_name}' already exists. Skipping creation.")
                return True
    else:
        logging.error(f"Tinybird - Failed to check existing data sources. Response: {response.text}")
    
    return False


def create_tinybird_datasource(event_name, schema):
    """Create a new Tinybird Data Source with the given schema if it does not exist."""
    url = f"https://api.{TINYBIRD_REGION}.tinybird.co/v0/datasources"
    headers = {"Authorization": f"Bearer {TINYBIRD_API_KEY}"}

    payload = {
        "name": event_name,
        "schema": schema,
        "format": "ndjson"
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        logging.info(f"Tinybird - Data Source '{event_name}' created successfully.")
        return True
    else:
        logging.error(f"Tinybird - Failed to create Data Source '{event_name}'. Response: {response.text}")
        return False


def fetch_linear_data(graphql_query, limit=None):
    """Fetch data from Linear API with pagination and optional limit."""
    linear_url = "https://api.linear.app/graphql"
    headers = {
        "Authorization": f"{LINEAR_API_KEY}",
        "Content-Type": "application/json"
    }

    all_records = []
    cursor = None
    total_fetched = 0

    while True:
        paginated_query = graphql_query.replace(
            "{pagination}", f'first: 50, after: "{cursor}"' if cursor else "first: 50"
        )

        response = requests.post(linear_url, headers=headers, json={"query": paginated_query})

        if response.status_code != 200:
            logging.error(f"Linear - HTTP {response.status_code} - Failed request to Linear API")
            logging.error(f"Linear - Response Text: {response.text}")
            return None

        response_data = response.json()

        if "errors" in response_data:
            logging.error(f"Linear - {response_data['errors']}")
            return None

        root_key = list(response_data["data"].keys())[0]  # E.g., "projects", "issues", "users"
        records = response_data.get("data", {}).get(root_key, {}).get("nodes", [])
        page_info = response_data.get("data", {}).get(root_key, {}).get("pageInfo", {})

        all_records.extend(records)
        total_fetched += len(records)

        if limit and total_fetched >= limit:
            all_records = all_records[:limit]
            break

        if not page_info.get("hasNextPage"):
            break

        cursor = page_info.get("endCursor")

    logging.info(f"Linear - Successfully fetched {len(all_records)} records.")
    return all_records


def send_to_tinybird(data, event_name, schema=None):
    """Send formatted JSONL data to Tinybird with an optional schema."""
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
            logging.info(f"Tinybird - Data successfully sent to {event_name}.")
            logging.info(f"Tinybird - {response_json['successful_rows']} rows ingested, {response_json['quarantined_rows']} quarantined.")
            return True
        elif response.status_code != 200:
            logging.error(f"Tinybird - HTTP {response.status_code} - Failed request to Tinybird")
            logging.error(f"Tinybird - Response Text: {response.text}")
            return False
        return True

    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending data to Tinybird: {e}")
        return False
