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

            orders.append({'restaurant': vendor, 'date': order_date,
                           'cost': cost, 'items': items,
                           'service': 'foodpanda'})

    return orders


# Get all deliveroo orders
def get_deliveroo_orders(orders):

    url = "https://deliveroo.com.sg/orders"

    cookies = {
            'cookie': '__cfduid=df92f1544373e416648f19b7367e064e71524824974; roo_guid=f13646f5-df6e-4829-b1ca-8a0d35c763ec; seen_cookie_message=t; session_data=eyJ1c2VyX2lkIjoxMDkwOTMwMiwic2Vzc2lvbl90b2tlbiI6IjYwNjk1OGEwNTU0MjQxOTI5ZTJlNjc3NWYwN2U3NmUwIn0.; consumer_auth_token=eyJhbGciOiJFUzI1NiIsImprdSI6Imh0dHBzOi8vZGVsaXZlcm9vLmNvLnVrL2lkZW50aXR5LWtleXMvMS5qd2sifQ.eyJleHAiOjE1MjQ4Mjg1ODAsImN1c3QiOjEwOTA5MzAyLCJzZXNzIjoid2ViLDYwNjk1OGEwNTU0MjQxOTI5ZTJlNjc3NWYwN2U3NmUwIn0.i7wn3RlhrRQSkkWX2dwnpKLrD2o-bzx2lzeu-qJhFr5NHHCzQEkx15fyer9W4Lwdy3G45CtT9d5IoL94HgG5yg; user_data=eyJpZCI6MTA5MDkzMDIsImVtYWlsIjoiY2d1cHRhMzE5QGdtYWlsLmNvbSIsImZpcnN0X25hbWUiOm51bGwsImxhc3RfbmFtZSI6bnVsbCwiZnVsbF9uYW1lIjoiQ2hhaXRhbnlhIEd1cHRhIiwicHJlZmVycmVkX25hbWUiOiJDRyIsInBob25lIjoiKzY1IDgyODMgNjcwNCJ9; api_auth=MTA5MDkzMDI6d2ViLDYwNjk1OGEwNTU0MjQxOTI5ZTJlNjc3NWYwN2U3NmUw; ajs_group_id=null; ajs_user_id=%2210909302%22; ajs_anonymous_id=%220a395f7c-b50f-4bbb-a067-d57ea70fda3e%22; __zlcmid=m8hIXTMT8ArKiS; location_data=eyJsb2NhdGlvbiI6eyJjb29yZGluYXRlcyI6WzEwMy43NTU3NTIsMS4zMTgyNzddLCJpZCI6bnVsbCwicG9zdF9jb2RlIjoiMTI3MDE3In19; __stripe_mid=f85803b4-c2eb-4228-8ffb-11253bf3274f; roo_session_guid=055b89dc-8f9c-4440-a674-90cbb268e44b; orderHelpInfo=eyJyZWRpcmVjdFRvIjoiLyJ9; locale=eyJsb2NhbGUiOiJlbiJ9; _orderweb_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWViMjg3YTA0NWM4OTU2YzdjMDYyODNkYTlmMDJhMzcxBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMWRqcmdNM1U3b3A1YWt1V3piUVVObEw0Z2orNEdRdmFSYkxpTm9saFpkeVk9BjsARg%3D%3D--4a7ae37ccc935c3f4095741c16bbc44177fa6d1e; roo_super_properties=eyJJUCBEZXRlY3RlZCBDaXR5IChJbmFjY3VyYXRlKSI6IlNpbmdhcG9yZSIsIklQIERldGVjdGVkIENvdW50cnkgKEluYWNjdXJhdGUpIjoiU0ciLCJjb250ZXh0Ijp7InVzZXJBZ2VudCI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDEwXzEyXzYpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS82Ni4wLjMzNTkuMTM5IFNhZmFyaS81MzcuMzYiLCJpcCI6IjEyMS43LjE3MC4xMTMiLCJsb2NhdGlvbiI6eyJjb3VudHJ5IjoiU2luZ2Fwb3JlIiwiY2l0eSI6IlNpbmdhcG9yZSJ9LCJsb2NhbGUiOiJlbiJ9LCJSZXF1ZXN0ZWQgTG9jYWxlIjoiZW4iLCJSb29Ccm93c2VyIjoiQ2hyb21lIiwiUm9vQnJvd3NlclZlcnNpb24iOiI2NiIsIkRldmljZSBUeXBlIjoiZGVza3RvcCIsIlRMRCI6InNnIiwiUGxhdGZvcm0iOiJ3ZWIiLCJPcmRlcnMgY291bnQiOjIsIkxvY2FsZSI6ImVuIiwibXZ0XzkxN19vcmRlcl9zdGF0dXMiOiJjd2EifQ..',
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

            orders.append({'restaurant': vendor,
                           'date': datetime.datetime.strptime(order_date, "%d %B %Y  %H:%M"),
                           'cost': cost, 'items': items, 'service': 'deliveroo'})

    return orders


if __name__ == "__main__":

    # Store all orders from foodpanda and deliveroo
    orders = []

    # List storing cookies for all users
    cookies = ['cookies for all users']

    # Get foodpanda order for all users
    for cookie in cookies:
        foodpanda_orders = get_foodpanda_orders(orders, cookie)

    # Get deliveroo orders
    orders = []
    deliveroo_orders = get_deliveroo_orders(orders)

    # Merge all orders from foodpanda and deliveroo
    fpanda_del_orders = foodpanda_orders + deliveroo_orders

    # Convert orders to pandas dataframe
    df = pd.DataFrame(fpanda_del_orders)

    # Export dataframe into csv file
    df.to_csv("fpanda_del_orders.csv", index=False)
