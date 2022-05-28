import yfinance as yf
import streamlit as st

from datetime import date, datetime
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go  # for interactive graphs
from get_all_tickers import get_tickers as gt


START = '2015-01-01'
TODAY = date.today().strftime("%Y-%m-%d")
st.title("Stock Prediction App")


# Liste erstellen sodass man aus allen Stocks die man sucht eine auswählen kann!!!!!!!!
stocks = ("AAPL", "GOOG", "MSFT", "GME")
selected_stock = st.selectbox("Select Dataset for prediction", stocks)


n_year = st.slider("Years of prediction:", 1, 4)
period = n_year * 365


@st.cache  # caches the data so it doesnt reload everytime
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)  # returns a panda dataframe
    data.reset_index(inplace=True)
    return data


data_load_state = st.text("Load Data ...")
data = load_data(selected_stock)
data_load_state.text("Loading Data ... Done!")

st.subheader("Raw Data")
st.write(data.tail())


def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_open'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='stock_close'))
    fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)


plot_raw_data()

# Forecasting
# needs a certain format

df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})
m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

st.subheader('Forecast Data')
st.write(forecast.tail())

st.write("Forecast Data")
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write("Forecast components")
fig2 = m.plot_components(forecast)
st.write(fig2)

