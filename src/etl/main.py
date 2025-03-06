import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import argparse
from utils.config_query import queries, schemas
from utils.helper import check_tinybird_datasource, create_tinybird_datasource, fetch_linear_data, send_to_tinybird

def main(data_type, limit):
    """Ensure Tinybird Data Source exists, then fetch and send data."""
    if data_type not in queries:
        print(f"Invalid data type: {data_type}. Choose from {list(queries.keys())}")
        return
    
    schema = schemas.get(data_type, None)

    # Step 1: Check if the Tinybird Data Source exists
    if not check_tinybird_datasource(data_type):
        if not create_tinybird_datasource(data_type, schema):
            print(f"Failed to create Tinybird Data Source: {data_type}")
            return

    # Step 2: Fetch Linear Data
    data = fetch_linear_data(queries[data_type], limit)

    # Step 3: Send Data to Tinybird
    if data:
        send_to_tinybird(data, data_type, schema)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Linear data from API and send to Tinybird.")
    parser.add_argument("data_type", help="Specify the data to query from Linear API (e.g., projects, issues)")
    parser.add_argument("--limit", type=int, help="Limit the number of records fetched", default=None)
    args = parser.parse_args()

    main(args.data_type, args.limit)