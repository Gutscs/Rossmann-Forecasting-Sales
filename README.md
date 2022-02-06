# Rossmann Store - Forecasting Sales

![](img/rossmann.jpg)

# 1. CONTEXT

Rossmann operates over 3,000 drug stores in 7 European countries. Currently, Rossmann store managers are tasked with predicting their daily sales for up to six weeks in advance. Store sales are influenced by many factors, including promotions, competition, school and state holidays, seasonality, and locality. With thousands of individual managers predicting sales based on their unique circumstances, the accuracy of results can be quite varied.

## 1.1. BUSINESS PROBLEM

The business problem can be defined by four topics as follows:

* **Motivation**
    * During a meeting, the Rossmann's CFO requested to the store managers a prediction of their daily sales for the next six weeks.

* **The problem's root cause**
    * The Rossmann's CFO wants to renovate each store by using part of the store's revenue in the next six weeks. 

* **The Stakeholder**
    * The CFO.

* **The solution format**
    * **Granularity:** Dailys sales for the next six weeks per Store
    * **Problem type:** Forecasting problem (Regression)
    * **Delivery method:** Cell phone access by using Telegram.


# 1. DATA

The datasets are in CSV format and can be found at the following kaggle link: https://www.kaggle.com/c/rossmann-store-sales/data.

## 1.1. FILES

The files used to the project are as follows:

* **train.csv** - historical data including Sales to train the model
* **test.csv** - historical data excluding Sales to test the model
* **store.csv** - supplemental information about the stores

## 1.2. DATA FIELDS

Most of the fields are self-explanatory. The following are descriptions for those that aren't.

* **Id:** an Id that represents a (Store, Date) duple within the test set
* **Store:** a unique Id for each store
* **Sales:** the turnover for any given day (this is what you are predicting)
* **Customers:** the number of customers on a given day
* **Open:** an indicator for whether the store was open: 0 = closed, 1 = open
* **StateHoliday:** indicates a state holiday. Normally all stores, with few exceptions, are closed on state holidays. Note that all schools are closed on public holidays and weekends. a = public holiday, b = Easter holiday, c = Christmas, 0 = None
* **SchoolHoliday:** indicates if the (Store, Date) was affected by the closure of public schools
* **StoreType:** differentiates between 4 different store models: a, b, c, d
* **Assortment:** describes an assortment level: a = basic, b = extra, c = extended
* **CompetitionDistance:** distance in meters to the nearest competitor store
CompetitionOpenSince[Month/Year] - gives the approximate year and month of the time the nearest competitor was opened
* **Promo:** indicates whether a store is running a promo on that day
* **Promo2:** Promo2 is a continuing and consecutive promotion for some stores: 0 = store is not participating, 1 = store is participating
* **Promo2Since[Year/Week]:** describes the year and calendar week when the store started participating in Promo2
* **PromoInterval:** describes the consecutive intervals Promo2 is started, naming the months the promotion is started anew. E.g. "Feb,May,Aug,Nov" means each round starts in February, May, August, November of any given year for that store