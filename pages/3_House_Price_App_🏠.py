
import streamlit as st
import pandas as pd
import plotly.express as px

from collections import defaultdict
from datetime import datetime

st.title('House Price App :house:')
st.write('This app will help you to estimate the house price in your area')

today = datetime.today()
first, second = st.columns(2)

with first:
    house_price = st.number_input('Enter the house list price (Not sell price)', value=300_000, step=5000, format='%d')
    principal_ammount = st.number_input('Enter the principal amount (How much you are borrowing)', value=250_000, step=1000, format='%d')
    mortgage_payment = st.number_input('Enter the mortgage payment', value=2000, step=100, format='%d')
    mortgage_rate = st.slider('Enter the mortgage rate (%)', min_value=0.0, max_value=10.0, value=5.50, step=0.05, format='%f')

with second:
    assessment_rate = st.number_input('Enter the house assessment value ($)', value=344_000, step=1_000, format='%d')
    house_type = st.selectbox('Select the house type', ['Bungalow', 'Semi-Detached', 'Townhouse'])
    annual_insurance = st.number_input('Annual Insurance Cost ($)', value=1098, step=10, format='%i')
    annual_maintenance = st.slider('Enter the annual maintenance (1%; StatsCan)', min_value=0.0, max_value=5.0, value=1.0, step=0.5, format='%f')
    
monthly_interest = -(principal_ammount * (mortgage_rate / 100) / 12)
monthly_maintenance = -(house_price * (annual_maintenance / 100) / 12)
monthly_insurance = -(annual_insurance / 12)
monthly_tax = -(assessment_rate * 0.028015 / 12)

left, right = st.columns([2, 3])
with left:
    monthly_data = {
            'Mortage': -mortgage_payment,
            'Maintenance': monthly_maintenance,
            'House Insurance': monthly_insurance,
            'Property Tax': monthly_tax}

    df = pd.DataFrame(monthly_data, index=['Monthly Cash Flow'])
    st.plotly_chart(px.bar(df, y=df.columns, title='Monthly Cash Flow', text_auto=True, orientation='v',
                    color_discrete_sequence=px.colors.qualitative.Pastel1, template='plotly_white'))

with right:
    # calculate equity
    projected_years = 10
    monthly_equity = defaultdict(list)
    # calculate monthly cash flow
    for i in range(1, projected_years + 1):
        monthly_equity['Interest'].append(monthly_interest * 12)
        monthly_equity['Principal'].append(mortgage_payment - monthly_interest)

    # plot a bar chart
    years = pd.date_range(today, periods=projected_years, freq='Y')
    df = pd.DataFrame(monthly_equity)
    df['Date'] = years
    st.plotly_chart(px.line(df, x='Date', y=df.columns, title='Yearly Equity',
                    color_discrete_sequence=px.colors.qualitative.Pastel1, template='plotly_white', width=600, height=600))


