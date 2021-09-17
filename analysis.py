#Libraries
#from dotenv import dotenv_values
import os
import requests
import pandas as pd
from bokeh.plotting import figure, output_file, save, show
from bokeh.models import DatetimeTickFormatter, NumeralTickFormatter, DatetimeTicker
from bokeh.embed import components


def stockAnalysis(ticker_symbol, ticker_date):
    #import .env file to protect API Key during local development
    #config = dotenv_values(".env")
    api_key = os.environ['API_KEY']

    #get the data from the AlphaVantage API
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker_symbol}&outputsize=full&apikey={api_key}'
    r = requests.get(url)
    data = r.json()

    #validation of user ticker symbol input
    if len(data.keys()) == 1:
        script = ''
        div = 'You entered a ticker symbol that does not exist. Please try again.'
        return script, div
    #Create a pandas dataframe with the data.
    df = pd.DataFrame(data['Time Series (Daily)']).T.reset_index()

    #set up the index as datetimes
    df['index'] = pd.to_datetime(df['index'], infer_datetime_format = True)
    df.set_index('index', drop = True, inplace = True)
    #rename columns
    df.columns = ['open','high','low','close','adjusted_close','volume','dividend_amt','split_coeff']


    #reduce data to a month
    month = df.loc[f'{ticker_date}']

    #validation of user date input
    if len(month) == 0:
        script = ''
        div = 'You entered a date that does not exist. Please try again.'
        return script, div

    #some variables for plotting labels
    months_list = ['January','February','March','April','May','June','July','August','September','October','November','December']
    ticker_symbol = data['Meta Data']['2. Symbol']
    ticker_title = f"{ticker_symbol} Stock Prices - {months_list[month.index.month[-1]-1]} {month.index.year[-1]}"

    #build the Bokeh figure
    p = figure(x_axis_type="datetime", sizing_mode="stretch_both",
               title=ticker_title, name='ticker_plot')
    p.xgrid.grid_line_color=None
    p.ygrid.grid_line_alpha=0.5

    p.xaxis.axis_label = 'Date'
    p.xaxis.formatter = DatetimeTickFormatter(days="%D")
    p.xaxis.ticker = DatetimeTicker(desired_num_ticks = int(len(month)/2))

    p.yaxis.axis_label = 'Price (per share)'
    p.yaxis[0].formatter = NumeralTickFormatter(format="$0.00")


    #add Bokeh renderers
    p.line(month.index, month.adjusted_close, legend_label="Closing Price (Adjusted)", line_color="purple", line_width=2)

    script, div = components(p)
    return script, div
