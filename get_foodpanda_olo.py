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

    # List storing cookies for all users
    cookies = ['__cfduid=d0dc7bc4366a7088f77119d2e6d9885731526195069; hl=en; AppVersion=f0d686d; ld_key=121.7.170.113; ld_flags_sum=0b61dd24806ba2d3590b7c80700d795d; PHPSESSID=e336b8c03966421ac3e8651646f61df7; token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpZCI6IjE3MzczYzhmZjMxN2QxMDQ4NjE1MzBmYTdlM2NjNmZhOGNlYThhZTciLCJjbGllbnRfaWQiOiJ2b2xvIiwidXNlcl9pZCI6ImNndXB0YTMxOUBnbWFpbC5jb20iLCJleHBpcmVzIjoxNTU3MzA5OTU1LCJ0b2tlbl90eXBlIjoiYmVhcmVyIiwic2NvcGUiOiJBUElfQ1VTVE9NRVIgQVBJX1JFR0lTVEVSRURfQ1VTVE9NRVIifQ.vrpAD-SnmbfDejk90sfXi2J6fsKXsT2TeyZzBEzL_IeEAHM-oc3V7BLA3lw1sWGkQ4JPSSgFgKW4OFJI5J1hjD85Ilf64Rgx8FneU9NI5PyVw-XKkO3EH4UmhVuWv__KyXut9zWXq8nkYpGYJxmLgqExdFamOJ5B0uo-tN2SohrizhUp65ILfF7u5mDe0Kt6ls-cMOrpkCiiXHrm-hNyn7mZLXQvPGO4nVapgt9rRs9_Oncvm8M5rClDM96Jgo-cPnNwzJsuu-wjZDwuFYY8A-1zYbKC5zJn6_yrMJkMKmp87EufK6UvxBT4Nmcmqq3hkojwj1rWfi3_GcGVELSwMA; tooltip-reorder=true',
               '__cfduid=d0dc7bc4366a7088f77119d2e6d9885731526195069; hl=en; AppVersion=f0d686d; ld_key=121.7.170.113; ld_flags_sum=0b61dd24806ba2d3590b7c80700d795d; tooltip-reorder=true; PHPSESSID=ec0c4cae50542d4f703f5ae1ed94bb0e; token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpZCI6IjkwYmEzZDNiZWVhMGZiM2ZjNGZlZWIzM2QwYjk2OTA2NjUyOTk1ZjgiLCJjbGllbnRfaWQiOiJ2b2xvIiwidXNlcl9pZCI6Im1lZ2huYTBzYXhlbmFAeWFob28uY28uaW4iLCJleHBpcmVzIjoxNTU3MzEwMTIzLCJ0b2tlbl90eXBlIjoiYmVhcmVyIiwic2NvcGUiOiJBUElfQ1VTVE9NRVIgQVBJX1JFR0lTVEVSRURfQ1VTVE9NRVIifQ.nzDnrpM5Tqkq4-1F1G-VxXsZTwXhTj78R6lOqgs8GymapyVFlIhYG1IeGqjcMSt83VwyV_Gjzaq-dMw3Kud-2ut4CjVfmJCxBR7e2nTPWuCS_XzURzdAxrIYoWava_Xlk3yloK2DUmSuC2EVn1GAhIh8x-lHnuHLbUF7iwrs2OClylVqok7I-KHcd-N0Z_VKMQUX-qmcj-MxfcA0EHVxP17a1Ax91Ek0mV-Eo_M5Q2yIQ-_-W0LFuOHN0uNN1R9iZr2W2dwJ3-uDvNzT-CIpLHn-gxooohEmwpbNAlQO_5AilVTAJDbySWOLSMTk3Lal3WlLo5qBUgQH0wV4xk_xjg; rider-banner-hidden=1']

    # Get foodpanda order for all users
    for cookie in cookies:
        foodpanda_orders = get_foodpanda_orders(orders, cookie)

    # Convert orders to pandas dataframe
    df = pd.DataFrame(orders)

    # Export dataframe into csv file
    df.to_csv("foodpanda_orders.csv", index=False)
