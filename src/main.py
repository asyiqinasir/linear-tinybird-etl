import argparse
from config_query import queries, schemas
from helper import fetch_linear_data, send_to_tinybird

def main(data_type):
    """Fetch data from Linear API and send to Tinybird."""
    if data_type not in queries:
        print(f"Invalid data type: {data_type}. Choose from {list(queries.keys())}")
        return

    data = fetch_linear_data(queries[data_type])

    if data:
        schema = schemas.get(data_type, None)
        send_to_tinybird(data, data_type, schema)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Linear data from API and send to Tinybird.")
    parser.add_argument("data_type", help="Specify the data to query from Linear API (e.g., projects, issues)")
    args = parser.parse_args()

    main(args.data_type)
