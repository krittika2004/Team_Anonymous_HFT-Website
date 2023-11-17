from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import pickle
import requests

app = Flask(__name__)
data1 = None
symbol=None

# Load the trained Random Forest model from the pickle file
with open('model.pkl', 'rb') as f:
    rf_model = pickle.load(f)

# print(data1)
def getValues(symbol, data1):
    headers = {
        'Content-Type': 'application/json'
    }

    # print(data1)

    url= f"https://api.tiingo.com/tiingo/daily/{symbol}/prices?startDate={data1}&token=f266d4430c18209e3c0b50f8f8f8d4d7eea001ab"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # Convert the response to JSON format
        data = response.json()
    
        # Initialize empty lists for each variable
        highs = []
        closes = []
        opens = []
        lows = []
        # volumes = []
    
        # Loop through the response data and extract required values
        for item in data:
            highs.append(item['high'])
            closes.append(item['close'])
            opens.append(item['open'])
            lows.append(item['low'])
            # volumes.append(item['volume'])
        return (highs, lows, opens, closes)  
    return (1,2,3,4)



# Printing first few values of each variable
    # print("Highs:", highs[:5])
    # print("Closes:", closes[:5])
    # print("Opens:", opens[:5])
    # print("Lows:", lows[:5])
    # print("Volumes:", volumes[:5])            


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle the form submission
        data1 = request.form['date']
        symbol1= request.form['symbol']
        print(data1, symbol1)
        highs, lows, opens, closes = getValues(symbol1, data1)
        print(data1)
        print(highs)
        print(lows)
        print(opens)
        print(closes)
    #GET endpoint
    return render_template('index.html')

@app.route('/after', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        # Handle the form submission
        data1 = request.form['date']
        symbol1= request.form['symbol']

        highs, lows, opens, closes = getValues(symbol1, data1)
        print(data1, symbol1)
        return redirect('/after.html', data1=data1, pred=closes[0], methods=["POST"])
        print(data1)
        print(highs)
        print(lows)
        print(opens)
    # GET endpoint
    return render_template('index.html')

# @app.route('/submit', methods=['POST'])
# def submit():
#     name = request.form['name']

#     # Do something with the form data

#     return redirect(url_for('success'))

# @app.route('/success')
# def success():
#     return render_template('after.html')

if __name__ == '__main__':
    app.run(debug=True)
