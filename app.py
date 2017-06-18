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
    
    return redirect(url_for('plot', name = name, items = items))

@app.route('/plot', methods=['GET','POST'])
def plot():
    name = request.args.get('name')
    items = request.args.get('items')
    print items
    # get webpage:
    web = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?ticker='+ name + '&qopts.columns=date' + items +'&api_key=vE8zyFxDsKyf5NnGyDdC'
    print web
    
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
    print list(df)
    
        
        # check if the post request has the file part
     #name = request.args.get('name')
    #df = request.files['file']
    #df = pd.DataFrame(df)
    #print list(df)
    #print df['date']
    
    def datetime(x):
        return np.array(x, dtype=np.datetime64)

    p1 = figure(title="Stock Prices")
    p1.grid.grid_line_alpha=0.3
    p1.xaxis.axis_label = 'Date'
    p1.yaxis.axis_label = 'Price'

    for i in range(1,len(list(df))):
        p1.line(df['date'], df['open'])
    
    p1.legend.location = "top_left"

    window_size = 30
    
    #script, div = components(p1)
    
    return render_template("plot.html", name=name)
  
if __name__ == '__main__':
  app.run(port=33507, host='0.0.0.0')
