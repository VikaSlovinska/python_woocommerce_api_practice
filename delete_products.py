"""
WooCommerce Product Deletion Script

This script connects to the WooCommerce API, retrieves product data, and allows the user to
delete products based on confirmation. It logs relevant information during the process.

- Author: ViktoriyaSlovinska

"""

import logging
import os
from woocommerce import API

# Setting up the logging configuration to display informational messages
logging.basicConfig(level=logging.INFO)

# WooCommerce API keys for authentication
woo_key = 'ck_1ffcec6023372bc9e82fb844e233ac00e32fe0f2'
woo_secret = 'cs_ba10a1f4ae4116788305140b2d4cb163b56c6341'


def check_environ_variables(variable_name):
    """
    Check if the specified environment variable is set. If not, log an error and raise an exception.

    Parameters:
    - variable_name (str): The name of the environment variable to check.
    """
    try:
        # Attempting to retrieve the value of the specified environment variable
        os.environ[variable_name]
    except KeyError as e:
        # If the environment variable is not set, log an error and raise an exception
        error_message = f"The environment variable must be set: {e}"
        logging.exception(error_message)
        raise Exception(error_message)


# Checking whether the WooCommerce API keys are set as environment variables
check_environ_variables(woo_key)
check_environ_variables(woo_secret)

# Initializing the WooCommerce API connection
wcapi = API(
    url="http://modamarket.local/",
    consumer_key=os.getenv(woo_key),
    consumer_secret=os.getenv(woo_secret),
    version="wc/v3",
    timeout=60
)

# Retrieving products from WooCommerce
page = 1
total_products = []
products_to_delete = []

while True:
    # Fetching products in batches of 100
    r = wcapi.get('products', params={'per_page': 100, 'page': page})
    products = r.json()
    page = page + 1

    # Checking if there are no more products
    if not products:
        break

# Populating lists with product IDs, and identifying products with no images
for product in products:
    total_products.append(product['id'])
    if not product['image']:
        products_to_delete.append(products['id'])


def delete_confirm():
    """
    Confirm deletion of products from the store and perform the deletion if the user agrees.
    """
    logging.info(f"There are {len(total_products)} products in your store.")
    delete = input(f"Are you sure you want to delete {len(products_to_delete)} products? (Yes/No): ").lower()

    if delete in ['yes', 'y']:
        # If the user agrees, delete the products from the database
        logging.info(f"Deleting products from the database...")
        for i in products_to_delete:
            wcapi.delete(f"products/{i}", params={'force': True})
    else:
        # If the user declines, log a message indicating no products have been deleted
        logging.info("No products have been deleted")


# Confirming deletion and logging results
delete_confirm()
logging.info(f"{len(products_to_delete)}\n"
             f"Products deleted. {len(total_products) - len(products_to_delete)}\n"
             f"Products remaining in your store.")
