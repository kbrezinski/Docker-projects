
from PIL import Image
import streamlit as st

st.title('Manitoba Lottery App :chart_with_downwards_trend:')

image = Image.open('images/649.png')
st.image(image, width=256)

options, actual, costs = st.columns(3)
choices = ('Bi-weekly', 'Weekly', 'Monthly')

# first column
with options:
    frequency = st.selectbox(
    'How often do you play the lottery?', choices)
    num_tickets = st.slider('How many tickets do you buy?', 1, 24, 1)
    num_years = st.slider('How many years have you played?', 1, 100, 1)
    plays_extra = st.checkbox('Do you play Extra?')

# second column
with actual:
    st.subheader('Realistic Loss')
    weekly_loss = -3.9928 if plays_extra else -2.9928

    if frequency == 'Bi-weekly':
        weekly_loss *= 2 * num_tickets
        st.metric(label="Bi-weekly Loss", value=f"${weekly_loss:.2f}", delta=f"-${weekly_loss*0.9184:.2f}")
    elif frequency == 'Weekly':
        weekly_loss *= num_tickets * num_tickets
        st.metric(label="Weekly Loss", value=f"${weekly_loss:.2f}", delta=f"-${weekly_loss*0.9184:.2f}")
    else:
        weekly_loss *= 0.25 * num_tickets
        st.metric(label="Monthly Loss", value=f"${weekly_loss:.2f}", delta=f"-${weekly_loss*0.9184:.2f}")

    yearly_loss = weekly_loss * 52
    st.metric(label="Yearly Loss", value=f"${yearly_loss:.2f}", delta=f"-${yearly_loss*0.9184:.2f}")
    term_loss = weekly_loss*52*num_years
    st.metric(label=f"{num_years} Year Loss", value=f"${term_loss:.2f}", delta=f"-${term_loss*0.9184:.2f}")


with costs:
    st.subheader('What did I Miss?')
    st.metric(label="Cups of Cofee", value=f"{weekly_loss / 2:.2f} ☕",
                delta=f"{weekly_loss/2*0.9184:.2f}")
    st.metric(label="Iphone SE", value=f"{yearly_loss / 600:.2f} 📱",
                delta=f"{yearly_loss/600*0.9184:.2f}")
    st.metric(label="Used Cars ", value=f"{term_loss / 8000:.2f} 🚗",
                delta=f"{term_loss/8000*0.9184:.2f}")

caption = '''
Realistic Losses are based on the average cost of a ticket and the average chance of winning 
over a typical persons lifespan of 85 years. This assumes that you play the lottery from the age of 
18 to 85, and that you play the lottery bi-weekly and buy the maximum number of tickets allowed my MB lottery
which is 25 tickets per draw. Theoretical losses are shown in red underneath the values.
These values are based on the average cost of a ticket and the average chance of winning over billions of
iterations, unrealistic for us but takes into account winning the jackpot multiple times and the payout. 
'''
st.caption(caption)
st.markdown("***")


st.subheader('Source Code')
with open('code/lottery.py', 'r') as f:
    code = f.read()

st.code(code, language='python')