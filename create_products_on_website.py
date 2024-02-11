
"""
This script creates a specified number of products on a WooCommerce website using the WooCommerce API.

Usage:
  python create_products_on_website.py --number_of_products=<num>

Arguments:
  --number_of_products=<num>: Specifies the number of products to create on the WooCommerce website.

Required Python modules:
  - woocommerce: Python wrapper for interacting with the WooCommerce REST API.
  - string: Provides string constants and operations for generating random strings.
  - random: Generates random numbers and strings.
  - argparse: Parses command-line arguments.

Example:
  $ python create_products_on_website.py --number_of_products=5

Ensure to replace the placeholder values of 'url', 'consumer_key', and 'consumer_secret' with actual values
corresponding to your WooCommerce website.

"""

from woocommerce import API
import string
import random
import argparse

parser = argparse.ArgumentParser(description="Process some integer")
parser.add_argument('--number_of_products', required=True, help='how many products to create')
args = parser.parse_args()
num_of_products = args.number_of_products


wcapi = API(
    url='http://modamarket.local/',
    consumer_key='ck_1ffcec6023372bc9e82fb844e233ac00e32fe0f2',
    consumer_secret='cs_ba10a1f4ae4116788305140b2d4cb163b56c6341',
    version='wc/v3',
    timeout=60
)

for i in range(int(num_of_products)):
    length = 15
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for _ in range(length))
    random_float = round(random.uniform(1, 100), 2)

    data = {
        "name": random_string,
        "regular_price": str(random_float),
        "price": random_float
    }

    rs_api = wcapi.post("products", data)

    # Check if the request was successful
    if rs_api.status_code == 201:  # Assuming 201 indicates successful creation
        try:
            rs_json = rs_api.json()
            name = rs_json.get('name')  # Using .get() to avoid KeyError if 'name' doesn't exist
            price = rs_json.get('price')  # Using .get() to avoid KeyError if 'price' doesn't exist
            if name is not None and price is not None:
                print(f"{i + 1} of {num_of_products} products created: {name}, {price}")
            else:
                print("Error: Response JSON does not contain expected data.")
        except ValueError:
            print("Error: Response is not in valid JSON format.")
    else:
        print("Error: Failed to create product. Status code:", rs_api.status_code)






