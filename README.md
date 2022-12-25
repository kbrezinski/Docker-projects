
# Streamlit-App

<a target="new"><img border=0 src="https://img.shields.io/badge/Python-3.9+-blue.svg?style=flat" alt="Python version"></a>

This is a simple streamlit app to show the power of streamlit. The app is deployed on heroku and can be accessed [here](). This repository was created to help my parents understand some basic concepts.

This repository contains:

1. `Stock Price App` - This app compares stock portfolio performance from some user defined stock ticker symbols. The user can select the company and the time period for which the stock price is to be shown. The app uses the `yfinance` library to fetch the stock price data. Useful for comparisons.
2. `Manitoba Lottery App` - This app calculations the net return from the lottery in Manitoba. Various user input parameters are used to calculate the costs of gambling in Manitoba's most popular lotteries.


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


