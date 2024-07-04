This program crawls reviews from Coupang to generate a bipartite graph data of users and products, where the weight of edges are review scores.

Usage
=================
Requirements
-----------------
* [Selenium](https://selenium-python.readthedocs.io/)

Input
-----------------
Set the entry keyword by changing the initial value of `search_queue`.

Output
-----------------
* `output.csv`: List of category number, product id, user id, number of photo, rating, date, number of people who thought it was helpful
* `category_code.csv`: List of indices and their corresponding cateogry id
* `user_code.csv`: List of indices and their corresponding user id
* `product_set`, `review_set`: Temporary file for storing current state of variables with the same name. Used to restore state of corresponding variables on restart.

Compatability
=================
The code is proven to work in May 2024. It may not work after security policy update in Coupang.
