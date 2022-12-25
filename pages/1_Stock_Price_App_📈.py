
import streamlit as st
import yfinance as yf
import pandas as pd

from datetime import datetime, timedelta

# user input
st.title('Stock Price App :chart_with_upwards_trend:')
num_days = st.number_input("Enter Number of Days to Track", min_value=1, max_value=720, value=14, step=7)
today_date = datetime.today()

Portfolio1, Portfolio2, Portfolio3 = st.columns(3)
defaults = ['AAPL', 'TSLA', '']
series = {}


for i, col in enumerate([Portfolio1, Portfolio2, Portfolio3]):
    with col:
        col.subheader(f'Portfolio {i+1}')

        symbols = st.text_input('Enter Stock Ticker Symbols', defaults[i],
                    placeholder="MSFT GOOGL", key=f"symbol{i}")

        # download data
        if symbols != '':
            data = yf.download(symbols, today_date - timedelta(days=num_days), today_date, group_by='column', threads=2)
            
            if data.empty:
                st.error(f'Invalid stock ticker {symbols}', icon="🚨")
                continue

            # plot data
            try:
                closing_price = data['Close'].iloc[:].sum(axis=1)
            except:
                closing_price = data['Close']
            base_price = closing_price[0]

            norm_price = closing_price.apply(lambda i: (i - base_price) / base_price * 100)
            series[symbols] = norm_price
    
            st.metric(label="Performance", value=f"{norm_price[-1]:.2f}%", delta=f"{closing_price[-1] - closing_price[0]:.2f}")
                

norm_port = pd.concat(series, axis=1)
st.line_chart(norm_port, use_container_width=True)