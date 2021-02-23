import pandas as pd
import streamlit as st
import yfinance as yf
import cufflinks as cf
import datetime

st.markdown('''
# Nifty 50 Stock Price App 
Shown are the stock price data for nifty listed companies.

**Credits**
- App built by [Baburaj R](https://linkedin.com/in/baburajr)
- Built in `Python` using `streamlit`, `yfinance`, `pandas` and `cufflinks`
''')
st.write('---')

# sidebar
st.sidebar.subheader('Query parameters')
start_date = st.sidebar.date_input("Start date", datetime.date(2019, 1, 1))
end_date = st.sidebar.date_input("End date", datetime.date(2021, 1, 31))

# scraping ticker data
ticker_list = pd.read_html('https://en.wikipedia.org/wiki/NIFTY_50')[1].drop(['Company Name', 'Sector'], axis=1)
tickerSymbol = st.sidebar.selectbox('Stock Ticker', ticker_list)
tickerData = yf.Ticker(tickerSymbol)
tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)

#ticker info
logo = '<img src="%s">' % tickerData.info['logo_url']
st.markdown(logo, unsafe_allow_html=True)

name = tickerData.info['longName']
st.header('**%s**' % name)

summary = tickerData.info['longBusinessSummary']
st.info(summary)

#ticker data
st.header('**Ticker Data**')
st.write(tickerDf)

st.header('**Bollinger Bands**')
qf = cf.QuantFig(tickerDf, title='First Quant Figure', legend='top', name='GS')
qf.add_bollinger_bands()
fig = qf.iplot(asFigure=True)
st.plotly_chart(fig)