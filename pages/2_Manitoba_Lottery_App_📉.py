
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
    weekly_loss = -3.9742 if plays_extra else -2.9753

    if frequency == 'Bi-weekly':
        weekly_loss *= 2 * num_tickets
        st.metric(label="Bi-weekly Loss", value=f"${weekly_loss:.2f}")
    elif frequency == 'Weekly':
        weekly_loss *= num_tickets * num_tickets
        st.metric(label="Weekly Loss", value=f"${weekly_loss:.2f}")
    else:
        weekly_loss *= 0.25 * num_tickets
        st.metric(label="Monthly Loss", value=f"${weekly_loss:.2f}")

    yearly_loss = weekly_loss * 52
    st.metric(label="Yearly Loss", value=f"${yearly_loss:.2f}")
    term_loss = weekly_loss*52*num_years
    st.metric(label=f"{num_years} Year Loss", value=f"${term_loss:.2f}")


with costs:
    st.subheader('What did I Miss?')
    st.metric(label="Cups of Cofee", value=f"{weekly_loss / 2:.2f} ☕ ")
    st.metric(label="Iphone SE", value=f"{yearly_loss / 600:.2f} 📱 ")
    st.metric(label="Used Cars ", value=f"{term_loss / 8000:.2f} 🚗 ")
   



#st.code(code, language='python')