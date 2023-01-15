
from mortgage import Mortgage 

import streamlit as st
import pandas as pd
import plotly.express as px

from datetime import datetime
from utils.constants import *
from utils.utils import compound_interest

st.title('House Price App :house:')
st.write('This app will help you to estimate the house price in your area')

today = datetime.today()
left_prompts, right_prompts = st.columns(2)

with left_prompts:
    house_price = st.number_input('Enter the house selling price ($)', value=375_000, step=5000, format='%d')
    down_payment = st.number_input('Enter your down payment (%)', value=20, step=1, format='%d')
    amort_period = st.number_input('Enter the amortization period (years)', value=25, step=1, format='%d')
    mortgage_rate = st.slider('Enter the mortgage rate (%)', min_value=0.0, max_value=10.0, value=5.50, step=0.05, format='%f')

with right_prompts:
    assessment_rate = st.number_input('Enter the house assessment value ($)', value=344_000, step=1_000, format='%d')
    house_type = st.selectbox('Select the house type', ['Bungalow', 'Semi-Detached', 'Townhouse'])
    annual_insurance = st.number_input('Annual House Insurance Cost ($)', value=1098, step=10, format='%i')
    annual_maintenance = st.slider('Enter the annual maintenance (1%; StatsCan)', min_value=0.0, max_value=5.0, value=1.0, step=0.5, format='%f')

# calculate some monthly constants
borrowed_ammount = house_price * (1 - down_payment / 100)
m = Mortgage(interest=mortgage_rate/100, amount=borrowed_ammount, months=amort_period*12)
monthly_payments = list(m.monthly_payment_schedule())
monthly_maintenance = -(house_price * (annual_maintenance / 100) / 12)
monthly_insurance = -(annual_insurance / 12)
monthly_tax = -((assessment_rate * ASSIN_MILL_RATE * 0.45) - 700) / 12

monthly_data = {
    'Maintenance': monthly_maintenance,
    'House Insurance': monthly_insurance,
    'Property Tax': monthly_tax,
    'Mortgage': -float(m.monthly_payment()),
    }

# show utilities
show_utils = st.checkbox('Include Utilities?', value=False)
if show_utils:
    water, elec, internet, other = st.columns(4)
    with elec:
        monthly_elec = st.number_input('Monthly Hydro Bill ($)', value=AVG_HYDRO_BILL, step=1, format='%i')
    with water:
        quart_water = st.number_input('Quarterly Water Bill ($)', value=AVG_QUART_WATER_BILL, step=1, format='%i')
    with internet:
        monthly_internet = st.number_input('Monthly Internet Bill ($)', value=AVG_INTER_BILL, step=1, format='%i')
        monthly_data['Water'] = -quart_water / 4
        monthly_data['Electricity'] = -monthly_elec
        monthly_data['Internet'] = -monthly_internet
    with other:
        monthly_other = st.number_input('Other Monthly Expenses ($)', value=0, step=1, format='%i')
        if monthly_other != 0: monthly_data['Other'] = -monthly_other

st.markdown("***")
st.title('Use this section to plot and forecast your monthly cash flow and equity')

# plot tabs
cash_flow, equity = st.tabs(['Monthly Cash Flow', "Equity Projection"])

# horizontal bar plots
with cash_flow:
    with st.expander('Additional Info'):
        st.write(f'''
        This plot shows the monthly cash flow for the house. The mortgage payment is split into two parts:
        1. Mortgage Equity portion: This is the amount that goes towards the principal amount of the mortgage. For you
            the amount is ${round(monthly_payments[0][0], 2)}.
        2. Mortgage Interest portion: This is the amount that goes towards the interest of the mortgage. For you
            the amount is ${round(monthly_payments[0][1], 2)}.
        **Because this is a monthly cash flow plot (money in/out your pocket), the equity portion is combined with the 
        mortgage payment as a negative value.** \n
        Also, the **Maintenance** portion includes all housing related expenses related to maintaining the house. It is 
        assumed homeowners will spend 1-1.5% of the house price on maintenance each year. This is based on StatsCan data.
        Think replacing your roof, furnace, floors, etc.
        ''')
    df = pd.DataFrame(monthly_data, index=['Monthly Cash Flow'])
    chart = px.bar(df.T, title='Monthly Cash Flow', text_auto=True, orientation='h', hover_data=['value'],
                    color_discrete_sequence=px.colors.qualitative.Pastel1, template='plotly_white', width=600, height=400)
    chart.update_traces(showlegend=False)
    st.plotly_chart(chart)
    
    col1, col2, col3 = st.columns(3)
    col1.metric('Monthly cash flow', f"${round(df.sum(axis=1)[0], 2)}")
    col2.metric('Mortgage Equity portion', f"${round(monthly_payments[0][0], 2)}")
    col3.metric('Mortgage Interest portion', f"${round(monthly_payments[0][1], 2)}")  
    st.markdown("***")
    df # prints the dataframe to screen

# equity plot
with equity:

    with st.expander('Input Explanation'):
        st.write('''
        - **Years to project**: How many years you want to project your equity. The default is 3 years.
        - **Plot rent**: Include rent in the equity plot. If you select this option, you will be asked to enter the monthly rent.
        - **Plot closing costs**: Include closing costs in the equity plot. Use a value close to 3-4% if you assume just buying your home. 
                    If you are buying and selling, use a value close to 6-7%.
        - **Plot appreciation**: Include house appreciation in the equity plot. Based on the house type you selected, the appreciation rate 
                    will be different. Default rate is based on 3Y, 5Y and 10Y average Manitoba selling prices.
        ''')

    # user inputs
    years_projected = st.slider('Years to project', min_value=1, max_value=amort_period, value=3, step=1, format='%i')
    left_inputs, center_inputs, right_inputs = st.columns(3)
    with left_inputs:
        plot_rent = st.checkbox('Plot rent?', value=False)
        if plot_rent: 
            rent = st.number_input('Enter the monthly rent ($)', value=2000, step=100, format='%i')
    with center_inputs:
        plot_closing = st.checkbox('Include closing costs?', value=False)
        if plot_closing: 
            closing_rate = st.number_input('Enter the closing costs (%)', value=3.0, step=0.5, format='%f')
    with right_inputs:
        plot_house = st.checkbox('Include appreciation?', value=False)
        if plot_house: 
            apprec_default = house_apprec_dict[house_type]
            house_appreciation = st.number_input('Enter the annual appreciation (%)', value=apprec_default*100, step=0.05, format='%.2f')

    # payments dataframe based on equity and interest
    payments_df = pd.DataFrame(
                monthly_payments, columns=['Equity', 'Interest'])\
                .cumsum()\
                .iloc[11::12, :]\
                .apply(pd.to_numeric, downcast='float')\
                .reset_index(drop=True)

    payments_df['Interest'] = payments_df['Interest'] * -1
    if plot_house:
        payments_df['Equity'] = payments_df['Equity'] + compound_interest(house_price, house_appreciation/100, amort_period) - house_price

    # annual outflows dataframe based on monthly data 
    monthly_data = {k:v for k,v in monthly_data.items() if k in ['Property Tax', 'Maintenance', 'House Insurance']}
    annual_outflows = {'Home Expenses': sum(monthly_data.values()) * 12}

    # add the rent if its selected
    if plot_rent: annual_outflows['Rent'] = -rent * 12

    # combine all the dataframes
    df = pd.concat([pd.DataFrame([annual_outflows], index=['Annual Outflows'])]*amort_period, ignore_index=True)

    # before the cumsum, add the closing costs if its selected
    if plot_closing: df['Home Expenses'][0] += -house_price * (closing_rate / 100)

    # concat the dataframes and calculate the net equity
    df = pd.concat([df.cumsum(), payments_df], axis=1)
    df['Net Equity'] = df[[col for col in df.columns if col != "Rent"]].sum(axis=1)
    df['Date'] = pd.date_range(today.strftime('%Y-%m'), periods=amort_period, freq='Y')
    df.set_index('Date', inplace=True)
    
    # plot line chart
    fig = px.line(df[:years_projected], title=f'Annual Equity Projection for {years_projected} years',
            color_discrete_sequence=px.colors.qualitative.Plotly, template='plotly_white', width=800, height=500)
    st.plotly_chart(fig)

    # show final metrics
    col1, col2, col3 = st.columns(3)
    col1.metric('Net Equity', f"${round(df[:years_projected]['Net Equity'][-1], 2)}")
    col2.metric('Equity portion (excl. down-payment)', f"${round(df[:years_projected]['Equity'][-1], 2)}")
    col3.metric('Interest portion', f"${round(df[:years_projected]['Interest'][-1], 2)}")  

    with st.expander('Show amortization table'):
        st.table(df[:years_projected])
