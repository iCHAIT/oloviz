# oloviz

**Vizualizing all food orders placed online**


online orders (**olo**) + **viz**ualizations = oloviz




### Scraping


* `get_foodpanda_olo.py` - Script for scraping foodpanda orders
* `get_deliveroo_olo.py` - Script for scraping deliveroo orders
* `merge_all_olo.py` - Script for combining orders from foodpanda, deliveroo, ubereats and domino's


### Dependencies

* [requests](http://docs.python-requests.org/en/master/)
* [beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [pandas](https://pandas.pydata.org/pandas-docs/stable/index.html)



### Working


* Go to the url of order history for website you are scraping data.

> Eg. https://www.foodpanda.sg/orders

* Then, open the Network's Tab in Developer Console

* Copy the request for the webpage as CURL command

* Use this [little tool](https://curl.trillworks.com/) to get the python code

* Use the cookies obtained from above in your code


### Note

For storing your cookies - 

### get_foodpanda_olo.py

In `main`, there is a list of cookies, if there are more than one users (as in my case), store cookies of all those users in a python list (separated by `,`). If there is only one user just save your cookie in that list.


### get_deliveroo_olo.py


For this script, update the below code snippet in the script with your own cookies.

```python
    cookies = {
                    'cookie': 'your cookies here',
    }
```



* I did not scrape orders from UberEats and Domino's and rather wrote them in manually, so you won't find script for scraping those websites.

* I save csv files for orders of all the services that I have used and finally use the `merge_all_olo.py` to create a consolidated file of orders `final_orders.csv` that I later import into Tableau for creating vizualizations.



# TODO's

* Accomodate for multiple users in `get_deliveroo_olo.py` - same as foodpanda script, mantain a list of cookies.
* Use selenium to scrape domino's orders.
* Cleanup and make `Items Ordered` more structured so that it easy to anayze that data field.
* Use a food database API to gather nutrition value of each meal and items.

### License

MIT © [Chaitanya Gupta](https://github.com/iCHAIT)