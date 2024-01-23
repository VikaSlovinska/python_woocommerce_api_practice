"""""

WooCommerce Product Data Export Script

This script retrieves product information from a WooCommerce store using the WooCommerce API
and saves the product names and prices to a CSV file.

Make sure to replace 'your_consumer_key' and 'your_consumer_secret' with your actual
WooCommerce API credentials before running the script.

Author: Viktoriya Slovinska
"""
from woocommerce import API
import csv
import os
# WooCommerce API initialization
wcapi = API(
     url="http://modamarket.local/",
     consumer_key="website_key",
     consumer_secret="website_secret",
     version="wc/v3",
     timeout=60
)
# Output CSV file name
outputfile = "products_and_prices_list.csv"
# List to store product information
products_list = []
# Page counter for pagination
page = 1
# Loop to retrieve products from WooCommerce
while True:
    r = wcapi.get("products", params={"per page" : 100, "page" : page})
    products = r.json()
# Check HTTP status code for success
    status_code = r.status.code
    response_body = r.content
    if status_code != 200:
        raise Exception (f"Expected status code is : 200,.\n"
                         f" Got: {status_code}. More info about response error:{response_body}")
    page = page + 1
# Break the loop if no more products
    if not products:
        break
# Extract product name and price and append to products_list
    for product in products:
        name = product['name']
        price = product['price']
        if price:
            products_list.append([name, price])
# Write product information to CSV file
with open(outputfile, 'w', newline='') as csv_f:
    writer = csv.writer(csv_f)
    writer.writerow(["name", "price"])
    writer.writerows(products_list)


