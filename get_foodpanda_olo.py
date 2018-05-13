import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# Get all foodpanda orders
def get_foodpanda_orders(orders, cookie):

    url = "https://www.foodpanda.sg/orders"

    cookies = {
        'cookie': cookie
    }

    resp = requests.get(url, cookies=cookies)

    html = resp.content

    soup = BeautifulSoup(html, 'html.parser')

    order_entry = soup.findAll('li')

    order_entry = list(set(order_entry))

    for order in order_entry:
        if order is not None:

            order_plc_date = order.find("h4", {"class": "vendor-name"})

            if order_plc_date is not None:
                vendor = order_plc_date.getText().strip().replace("\n", "").split(",", 1)[0]

                order_date = order_plc_date.find("span", {"class": "order-date"}).getText().strip()
                order_date = datetime.datetime.strptime(order_date, "%d %b, %Y")
            else:
                continue

            bill = order.find("div", {"class": "total"})

            if bill is not None:
                cost = bill.getText().replace(" ", "").replace("\n", "").split(':')[1]

            contents = order.find("ul", {"class": "order-product-list"})

            if contents is not None:
                food = contents.getText().split("\n")
                items = [i.strip() for i in food if i.strip()]

            orders.append({'Restaurant': vendor, 'Date': order_date,
                           'Cost': cost, 'Items': items,
                           'Service': 'foodpanda'})

    return orders


if __name__ == "__main__":

    # Store all orders in a list
    orders = []

    # Store cookies for all your users in this python list
    # If only 1 user then just place cookie for that user
    cookies = ['cookie for user 1', 'cookies for user 2']

    # Get foodpanda order for all users
    for cookie in cookies:
        foodpanda_orders = get_foodpanda_orders(orders, cookie)

    # Convert orders to pandas dataframe
    df = pd.DataFrame(orders)

    # Export dataframe into csv file
    df.to_csv("foodpanda_orders.csv", index=False)
