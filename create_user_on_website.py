
"""
Script to create multiple users on a WooCommerce website using the WooCommerce API.

Dependencies:
- woocommerce: Python interface for WooCommerce API
- uuid: Generates unique identifiers
- argparse: Parses command-line arguments
- logging: Configures and manages log messages
"""

import woocommerce
from woocommerce import API
import uuid
import argparse
import logging
import os

# Command-line argument parsing
parser = argparse.ArgumentParser(description='Process some integers')
parser.add_argument('--number_of_users', required=True, help='How many users to create')
args = parser.parse_args()
num_of_users = args.number_of_users

# Logging configuration
logging.basicConfig(filename='create_user.log', level=logging.DEBUG,
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

# WooCommerce API keys
variable_key = "site_key_variable"
variable_secret = "site_secret_varibale"

def check_env_variables():
    """
    Check if the required environment variables are set.
    Raises an exception if any of them is missing.
    """
    try:
        os.environ[variable_key]
    except Exception as e:
        logging.exception(f"The environment variable must be set: {e}")
        print(f"Error has occurred: {e}")
        raise Exception("Environment variables must be set")

    try:
        os.environ[variable_secret]
    except Exception as e:
        logging.exception(f"The environment variable must be set: {e}")
        print(f"Error has occurred: {e}")
        raise Exception("The environment variable must be set")

# Check environment variables
check_env_variables()

# WooCommerce API configuration
wcapi = API(
    url="http://modamarket.local/",
    consumer_key=os.getenv(variable_key),
    consumer_secret=os.getenv(variable_secret),
    version="wc/v3",
    timeout=60
)

# User creation loop
for i in range(int(num_of_users)):
    data = {'email': f'{uuid.uuid4()}@supersqa.com',
            'password': str(uuid.uuid4())}

    rs_api = wcapi.post("customers", data)
    rs_json = rs_api.json()
    email = rs_json['email']

    user_info = f"{i + 1} users added to website", f"User's email is: {email}"
    logging.info(user_info)
    print(user_info)





