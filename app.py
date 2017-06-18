from flask import Flask, render_template, request, redirect, url_for
import requests
import json
import simplejson
import pandas as pd

import numpy as np
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from bokeh.util.string import encode_utf8
from bokeh.io import hplot

#from form import SiteForm

#from __future__ import print_function

app = Flask(__name__)
app.config['DEBUG'] = True

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
    #print items
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
    print df['close']
    print df['adj_close']
    
    #print df['close']
    # check if the post request has the file part
     #name = request.args.get('name')
    #df = request.files['file']
    #df = pd.DataFrame(df)
    #print list(df)
    #print df['date']
    
    def datetime(x):
        return np.array(x, dtype=np.datetime64)

    #p1 = figure(x_axis_type="datetime", title="")
    #p1.grid.grid_line_alpha=0.3
    #p1.xaxis.axis_label = 'Date'
    #p1.yaxis.axis_label = 'Price'

    
    colors = ['#A6CEE3', '#B2DF8A', '#33A02C', '#FB9A99']
    
    plots = [None]*(len(list(df))-1)
    
    for i in range(1,len(list(df))):
        plots[i-1] = figure(x_axis_type="datetime", title=list(df)[i])

        plots[i-1].grid.grid_line_alpha=0.1
        plots[i-1].xaxis.axis_label = 'Date'
        plots[i-1].yaxis.axis_label = 'Price'
        
        y = df[list(df)[i]]
        #print y
        x = df['date']
        #print df['date']
        
        plots[i-1].line(datetime(x), y, color=colors[i-1], legend = list(df)[i])
        
    p = hplot(*plots)
      
    #p1.line(datetime(df['date']), df['close'])
    
    #p1.legend.location = "top_left"

    #window_size = 30
    
    script, div = components(p)
    
    return encode_utf8(render_template("plot.html", name=name, script = script, div=div))
  
if __name__ == '__main__':
  #port = int(os.environ.get("PORT", 33507))
  app.run(host='0.0.0.0', port=33507)
