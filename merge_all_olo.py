import pandas as pd


# fpanda_del_orders = pd.read_csv("fpanda_del_orders.csv")

foodpanda_orders = pd.read_csv("foodpanda_orders.csv")
deliveroo_orders = pd.read_csv("deliveroo_orders.csv")

ubereats_orders = pd.read_csv("uber_orders.csv", usecols=["Cost", "Date", "Items", "Restaurant", "Service"])

dominos_orders = pd.read_csv("dominos_orders.csv", usecols=["Cost", "Date", "Items", "Restaurant", "Service"])


# print(foodpanda_orders)
# print(deliveroo_orders)

# print(dominos_orders)
# print(dominos_orders)

# Important for getting correct datesbundle install
ubereats_orders['Date'] = pd.to_datetime(ubereats_orders.Date).dt.date

dominos_orders['Date'] = pd.to_datetime(dominos_orders.Date).dt.date

# Append ubereats orders to foodpanda and deliveroo
# final_orders = fpanda_del_orders.append(ubereats_orders, ignore_index=True)

# Append dominos orders to foodpanda, deliveroo and ubereats
# final_orders = final_orders.append(dominos_orders, ignore_index=True)

final_orders = pd.DataFrame()

final_orders = final_orders.append([foodpanda_orders, deliveroo_orders,
                                    ubereats_orders, dominos_orders], ignore_index=True)

final_orders.index += 1
final_orders.to_csv("final_orders.csv", index_label="Order Number")
