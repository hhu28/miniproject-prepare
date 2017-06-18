from flask import Flask, render_template, request, redirect, url_for
import requests
import json
import simplejson
import pandas as pd

import numpy as np
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file
#from form import SiteForm

#from __future__ import print_function

app = Flask(__name__)
#app.config.from_object(__name__)
#app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

# def getitem(obj, item):
#   return obj[item]

# def getinput():
#   args = request.args
#   name = getitem(args, 'name')
#   cp = getitem(args, 'type1')
#   acp = getitem(args, 'type2')
#   op = getitem(args,'type3')
#   aop = getitem(args, 'type4')

#   return name, cp, acp, op, aop

# Extract data by company name (may by date later)
# def extractData():  
#   web = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?ticker='+ name + '&qopts.columns=date' +'&api_key=vE8zyFxDsKyf5NnGyDdC'
#   r = requests.get(web)
#   jdata = simplejson.dumps(r.json())
#   datadict = simplejson.loads(jdata)['datatable']

#   # get column names 
#   names = []
#   for i in range(len(datadict['columns'])):
#     names.append(datadict['columns'][i]['name']) 
    
#   df = pd.DataFrame(datadict['data'],  columns= names)
#   # convert to data frame
#   return df

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/input', methods=['GET','POST'])  
def input():
  #form = SiteForm(request.form)
  if request.method == 'POST':
    name = request.form['name']    
    if name == '':
      name = 'fb'
    selected = request.form.getlist('price')
    
    items = ''
    for i in range(len(selected)):
        items = items + ',' + selected[i]
    
    # get webpage:
    web = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?ticker='+ name + '&qopts.columns=date' + items +'&api_key=vE8zyFxDsKyf5NnGyDdC'
    #print web
    
    # get data
    r = requests.get(web)
    jdata = simplejson.dumps(r.json())
    datadict = simplejson.loads(jdata)['datatable']
    
    #get column names 
    names = []
    for i in range(len(datadict['columns'])):
        names.append(datadict['columns'][i]['name']) 
    
    # convert to dataframe
    df = pd.DataFrame(datadict['data'],  columns= names)
    #print list(df)
    return redirect(url_for('plot', name=name, df = df))


@app.route('/plot', methods=['GET','POST'])  
def plot():
    name = request.args.get('name')
    df = request.args.get('df')
    
    def datetime(x):
        return np.array(x, dtype=np.datetime64)

    p1 = figure(x_axis_type="datetime", title="Stock Closing Prices")
    p1.grid.grid_line_alpha=0.3
    p1.xaxis.axis_label = 'Date'
    p1.yaxis.axis_label = 'Price'

    p1.line(datetime(AAPL['date']), AAPL['adj_close'], color='#A6CEE3', legend='AAPL')
    p1.line(datetime(GOOG['date']), GOOG['adj_close'], color='#B2DF8A', legend='GOOG')
    p1.line(datetime(IBM['date']), IBM['adj_close'], color='#33A02C', legend='IBM')
    p1.line(datetime(MSFT['date']), MSFT['adj_close'], color='#FB9A99', legend='MSFT')
    p1.legend.location = "top_left"

    aapl = np.array(AAPL['adj_close'])
    aapl_dates = np.array(AAPL['date'], dtype=np.datetime64)

    window_size = 30
    window = np.ones(window_size)/float(window_size)
    aapl_avg = np.convolve(aapl, window, 'same')
    
    script, div = components(p1)
    
    return render_template("plot.html", name=name)
  
if __name__ == '__main__':
  app.run(port=33507, host='0.0.0.0')
