import pandas as pd


fpanda_del_orders = pd.read_csv("fpanda_del_orders.csv")

ubereats_orders = pd.read_csv("uber_orders.csv", usecols=["cost", "date", "items", "restaurant", "service"])

dominos_orders = pd.read_csv("dominos_orders.csv", usecols=["cost", "date", "items", "restaurant", "service"])

# Important for getting correct datesbundle install
ubereats_orders['date'] = pd.to_datetime(ubereats_orders.date)

dominos_orders['date'] = pd.to_datetime(dominos_orders.date)

# Append ubereats orders to foodpanda and deliveroo
final_orders = fpanda_del_orders.append(ubereats_orders, ignore_index=True)

# Append dominos orders to foodpanda, deliveroo and ubereats
final_orders = final_orders.append(dominos_orders, ignore_index=True)

final_orders.index += 1
final_orders.to_csv("final_orders.csv", index_label="Order Number")
