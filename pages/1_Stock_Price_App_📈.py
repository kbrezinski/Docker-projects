
import streamlit as st
import yfinance as yf
import pandas as pd

from datetime import datetime, timedelta, time

st.title('Stock Price App :chart_with_upwards_trend:')

@st.cache()
def get_today_date():
    return datetime.today()
today_date = get_today_date()

# show slider if ytd is not selected
start_time, end_time = st.slider(
        "Enter Date Range for your Portfolios",
        min_value=today_date - timedelta(days=365*5),
        value=(today_date - timedelta(days=365), today_date),
        step=timedelta(days=30),
        format="MM/DD/YY")

# user inputs
left, right = st.columns(2)
with left:
    st.write(f"Selected Date Range: {start_time.strftime('%Y-%m-%d')} - {end_time.strftime('%Y-%m-%d')}")

with right:
    ytd = st.checkbox('Year To Date (:exclamation: Overrides the Slider :exclamation:)', value=False)
    if ytd:
        start_time, end_time = datetime(today_date.year, 1, 1, 1, 1), today_date

st.markdown('---')

# Portfolio Inputs
ticker_defaults = ['SPY', 'EWC', 'TSLA META AMZN GOOGL MSFT']
port_names = ['Portfolio 1', 'Portfolio 2', "Dad's Picks"]
series = {}

# Portfolio Plots
portfolio_plots = st.columns(3)
for i, col in enumerate(portfolio_plots):
    with col:
        col.subheader(port_names[i])
        symbols = st.text_input('Enter Stock Ticker Symbols', ticker_defaults[i],
                            placeholder="MSFT GOOGL", key=f"symbol{i}").upper()
        # download data
        if symbols != '':
            data = yf.download(symbols, start_time, end_time, group_by='column', threads=2)
            
            if data.empty:
                st.error(f'Invalid stock ticker {symbols}', icon="🚨")
                continue
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