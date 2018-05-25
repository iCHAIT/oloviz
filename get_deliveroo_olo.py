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
                    'cookie': '__cfduid=da74aa999974cfb430ca712ce57c4e2f81526195087; roo_guid=2d341e88-1eae-4286-96e9-411e8a22290f; seen_cookie_message=t; locale=eyJsb2NhbGUiOiJlbiJ9; roo_session_guid=52f900d3-2436-4e1b-b5bb-311e2c73d7e1; orderHelpInfo=eyJyZWRpcmVjdFRvIjoiLyJ9; browse_data=eyJkZWxpdmVyeV9kYXkiOiJ0b2RheSIsImRlbGl2ZXJ5X3RpbWUiOiJBU0FQIiwibG9jYXRpb24iOnsiY29vcmRpbmF0ZXMiOlsxMDMuNzU1NzUyLDEuMzE4Mjc3XSwiaWQiOm51bGwsInBvc3RfY29kZSI6IjEyNzAxNyJ9fQ..; location_data=eyJsb2NhdGlvbiI6eyJjb29yZGluYXRlcyI6WzEwMy43NTU3NTIsMS4zMTgyNzddLCJpZCI6bnVsbCwicG9zdF9jb2RlIjoiMTI3MDE3In19; _orderweb_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTk5MjUwM2YxMjI2MmRkNmNiNGQ5NDMwYzZlMTA0YjQwBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMWRWcEIzSi80U1pVSmxkL3FuSUFmNFR5QVFNNmpJK21sWmtkWmtUQm5DTzA9BjsARg%3D%3D--41be158f90c40f8fac763f5d8b2a8b6efc3aaa99; __stripe_mid=e71f8b1b-c830-46ef-a0dc-495c935c6138; session_data=eyJ1c2VyX2lkIjoxMDkwOTMwMiwic2Vzc2lvbl90b2tlbiI6IjUyYjliOGQxNjcwNjQxMDE5N2RmYjAyMzZjNzA0MzE0In0.; consumer_auth_token=eyJhbGciOiJFUzI1NiIsImprdSI6Imh0dHBzOi8vZGVsaXZlcm9vLmNvLnVrL2lkZW50aXR5LWtleXMvMS5qd2sifQ.eyJleHAiOjE1MjcwODU0NTksImN1c3QiOjEwOTA5MzAyLCJzZXNzIjoid2ViLDUyYjliOGQxNjcwNjQxMDE5N2RmYjAyMzZjNzA0MzE0In0.g-_I0ErFk-Ra6qA2LTdL-sFCm8PAMKsFLWjCLmEfU1_B0Q16xurLcmImUvnQdOurHCJB9QjwFLtAK-x9KaI5sw; user_data=eyJpZCI6MTA5MDkzMDIsImVtYWlsIjoiY2d1cHRhMzE5QGdtYWlsLmNvbSIsImZpcnN0X25hbWUiOm51bGwsImxhc3RfbmFtZSI6bnVsbCwiZnVsbF9uYW1lIjoiQ2hhaXRhbnlhIEd1cHRhIiwicHJlZmVycmVkX25hbWUiOiJDRyIsInBob25lIjoiKzY1IDgyODMgNjcwNCJ9; api_auth=MTA5MDkzMDI6d2ViLDUyYjliOGQxNjcwNjQxMDE5N2RmYjAyMzZjNzA0MzE0; __zlcmid=mYhMVpVil1YfuY; roo_super_properties=eyJJUCBEZXRlY3RlZCBDaXR5IChJbmFjY3VyYXRlKSI6IlNpbmdhcG9yZSIsIklQIERldGVjdGVkIENvdW50cnkgKEluYWNjdXJhdGUpIjoiU0ciLCJjb250ZXh0Ijp7InVzZXJBZ2VudCI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDEwXzEyXzYpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS82Ni4wLjMzNTkuMTM5IFNhZmFyaS81MzcuMzYiLCJpcCI6IjEyMS43LjE3MC4xMTMiLCJsb2NhdGlvbiI6eyJjb3VudHJ5IjoiU2luZ2Fwb3JlIiwiY2l0eSI6IlNpbmdhcG9yZSJ9LCJsb2NhbGUiOiJlbiJ9LCJSZXF1ZXN0ZWQgTG9jYWxlIjoiZW4iLCJSb29Ccm93c2VyIjoiQ2hyb21lIiwiUm9vQnJvd3NlclZlcnNpb24iOiI2NiIsIkRldmljZSBUeXBlIjoiZGVza3RvcCIsIlRMRCI6InNnIiwiUGxhdGZvcm0iOiJ3ZWIiLCJPcmRlcnMgY291bnQiOjQsIkxvY2FsZSI6ImVuIiwibXZ0XzkxN19vcmRlcl9zdGF0dXMiOiJjd2EifQ..; ajs_group_id=null; ajs_user_id=%2210909302%22; ajs_anonymous_id=%2249e4c400-ed03-4cd3-8982-48e78337642c%22',
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
