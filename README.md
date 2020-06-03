Data Analytics Tool Capstone with Lockheed Martin 
====
Overview
-----
This is a Lockheed Martin capstone project developed by a UW team. This project aims to provide `prognostic data analysis` for MOSFET  failure pattern. It consist of three parts: an `ETL database` to handle several terabytes of raw data, a `data analytics capability` to perform predictive health monitoring and assist in failure analysis and a `streamlined user interface` to visualize and extract parsed datasets. The ETL part consists of extract, transform and (up)load part. The user interface uses the awesome Flask framework combined with React and the Altair library makes it easy to create interactive visualization without writing any client side code. Besides, the mouse over effect is powered by Vega-tooltip.

Dependencies
----
Flask and data processing:
* Flask
* Altair
* Parquet
* Numpy
* Pandas

User interface:
* Altair
* React

Running
----
#### To run it in your local environment:
```
$ git clone https://github.com/lemoncyb/flasked-altair.git 
$ cd flasked-altair
$ python ./app.py
```
Visit [http://localhost:5000](http://localhost:5000) in your browser, that's it!
#### To run it as a web application:
We have already deployed it in Heroku. Visit [Capstone Project](https://capstone-lm.herokuapp.com/) and you will see it!

FAQs
----
#### Why I cannot see the Altair interactive charts?
Altair in Python is based on Vega, which builds upon Chrome engine. If you are using other browsers, try to switch to Chrome of latest version and clear browsing data.
