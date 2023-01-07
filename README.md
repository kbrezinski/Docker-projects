
# Streamlit-App

<a target="new"><img border=0 src="https://img.shields.io/badge/Python-3.9+-blue.svg?style=flat" alt="Python version"></a>
<a target="new"><img border=0 src="https://img.shields.io/website?down_color=red&down_message=offline&up_color=green&up_message=online&url=https%3A%2F%2Fkenneth-app.herokuapp.com%2F" alt="Website"></a>


This is a simple streamlit app to show the power of streamlit. The app is deployed on heroku and can be accessed [here](https://kenneth-app.herokuapp.com/). This repository was created as a fun project for my parents.

This repository contains:

1. `Stock Price App 📈` - This app compares stock portfolio performance from some user defined stock ticker symbols. The user can select the company and the time period for which the stock price is to be shown. The app uses the `yfinance` library to fetch the stock price data. Useful for comparisons.
2. `Manitoba Lottery App 📉` - This app calculations the net return from the lottery in Manitoba. Various user input parameters are used to calculate the costs of gambling in Manitoba's most popular lotteries.
3. `House Price App 🏠` - This app calculates the monthly mortgage payment for a house. The user can input the house price, down payment, interest rate and the amortization period. The app also computes the equity in the house over a period of time.


## Table of Contents
- [Streamlit-App](#streamlit-app)
  - [Table of Contents](#table-of-contents)
  - [Install](#install)
  - [Usage](#usage)

---

## Install
Install `Streamlit-App` using `pip`:
```
$ pip install -r requirements.txt
```

To install `Streamlit-App` using Docker run the following command:
```bash
$ docker build -t streamlit-app .
```

## Usage
Run the streamlit app using the following command:
```bash
$ streamlit run Home.py
```


