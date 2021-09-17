from flask import Flask, render_template, request, redirect, url_for
from forms import StockForm
from analysis import stockAnalysis


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Humb07dt$@ve$TheD@y!'


@app.route('/', methods=['GET','POST'])
def index():
    symbol = 'IBM'
    year_month = '1999-11'
    stock_form = StockForm()
    if stock_form.validate_on_submit():
        symbol = stock_form.ticker.data.upper()
        year_month = stock_form.ticker_date.data.strftime('%Y-%m')
    script, div = stockAnalysis(symbol, year_month)
    return render_template('index.html',
                            template_form=stock_form,
                            template_symbol=symbol,
                            template_date=year_month,
                            script=script, div=div)

@app.route('/about')
def about():
    return render_template('about.html')

##### Future separate results page? Currently can't get the data from the stock form to pass to this page correctly.
# @app.route('/result')
# def result():
#     if len(request.form) > 0:
#         symbol = request.form['ticker']
#         year_month = request.form['ticker_date']
#     return render_template('result.html', template_symbol=symbol, template_date=year_month)

if __name__ == '__main__':
  app.run(port=33507)
