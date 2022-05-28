# import get_all_tickers.get_tickers
import yfinance as yf
import streamlit as st

from datetime import date
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go  # for interactive graphs
import pandas as pd
import csv



# https://github.com/luigibr1/Streamlit-StockSearchWebApp/blob/master/web_app_v3.py
# https://share.streamlit.io/daniellewisdl/streamlit-cheat-sheet/app.py
# https://www.ritchieng.com/pandas-multi-criteria-filtering/

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


hide_dataframe_row_index = """
    <style>
    .row_heading.level0 {display:none}
    .blank {display:none}
    </style>
    """

# Local CSS Sheet
local_css("style.css")

START = '2015-01-01'
TODAY = date.today().strftime("%Y-%m-%d")


def load_data(ticker):
    data = yf.download(ticker, START, TODAY)  # returns a panda dataframe
    data.reset_index(inplace=True)
    return data


# Global variables
st.title("Stock Web-App")
page = st.selectbox("Stock Information or List of Companies", ["Stock Information", "List of Companies"])
st.sidebar.subheader("""**Stock Search Web App**""")
selected_stock = st.sidebar.text_input("Enter a valid stock ticker")
button_clicked = st.sidebar.button("GO")
data = load_data(selected_stock)

###################################
# Einlesen der CSV Datei um die Ticker Names ausgeben zu lassen
file = open("Top100_Company_Tickers.csv")
csvreader = csv.reader(file)
print(csvreader)
header = []
header = next(csvreader)
name = []
dict_tickers = {}

for rows in csvreader:
    dict_tickers.update({rows[0]: rows[1]})
file.close()


###################################


def main():
    pass

if button_clicked == "GO":
    main()


def plot_raw_data():
    st.subheader("""Daily **closing price** for """ + selected_stock)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='Closing Price'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Opening Price'))
    fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)


def main():
    if page == "Stock Information":
        plot_raw_data()
        forecasting()

    if page == "List of Companies":
        Table_Ticker()


# Methode um zu Beginn direkt eine Aktie anzeigen zu lassen
def startData():
    selected_stock = 'AAPL'
    data = load_data(selected_stock)
    st.write(data)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_open'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='stock_close'))
    fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

def Table_Ticker():
    data_items = dict_tickers.items()
    print(list(data_items))
    data_list = list(data_items)
    df = pd.DataFrame(data_list)
    df.columns = ['Ticker Name', 'Company Name']
    st.table(df)


def forecasting():
    n_year = st.slider("Years of prediction:", 1, 4)
    period = n_year * 365
    df_train = data[['Date', 'Close']]
    df_train = df_train.rename(columns={'Date': "ds", "Close": "y"})
    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)
    st.subheader('Forecast Data')
    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1)



if __name__ == "__main__":
    main()
