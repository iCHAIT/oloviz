import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# Get all deliveroo orders
def get_deliveroo_orders(orders):

    url = "https://deliveroo.com.sg/orders"

    cookies = {
                    'cookie': 'your cookies here',
    }

    resp = requests.get(url, cookies=cookies)

    html = resp.content

    soup = BeautifulSoup(html, 'html.parser')

    order_history = soup.find("div", {"class": "user user--history mbottom30"})

    order_entry = order_history.findAll("li")

    for order in order_entry:
        if order is not None:

            items = []

            vendor = order.find("span", {"class": "history-restaurant"}).getText().strip()
            order_date = order.find("span", {"class": "history-col-date"}).getText().strip()

            cost = order.find("span", {"class": "history-col-amount"}).getText().strip()

            order_endp = order.find(href=True)

            order_url = url + "/" + order_endp['href'].split("/")[2]

            resp = requests.get(order_url, cookies=cookies)

            html = resp.content
            soup = BeautifulSoup(html, 'html.parser')

            inner_order_entry = soup.find("div", {"class": "order-list-inner"})

            if inner_order_entry is None:
                continue

            detailed_orders = inner_order_entry.findAll("div", {"class":"oi-inner"})

            for detail in detailed_orders:
                if detail is not None:
                    qnt = detail.find("div", {"class": "oi-quantity"}).getText().strip()
                    items.append(qnt + " " + detail.find("div", {"class": "oi-title"}).getText().strip())

                    sides = detail.findAll("li")

                    for side in sides:
                        items.append(side.getText())

            orders.append({'Restaurant': vendor,
                           'Date': datetime.datetime.strptime(order_date, "%d %B %Y  %H:%M").date(),
                           'Cost': cost, 'Items': items, 'Service': 'deliveroo'})

    return orders


if __name__ == "__main__":

    # Store all orders in a list
    orders = []

    deliveroo_orders = get_deliveroo_orders(orders)

    # Convert orders to pandas dataframe
    df = pd.DataFrame(orders)

    # Export dataframe into csv file
    df.to_csv("deliveroo_orders.csv", index=False)
