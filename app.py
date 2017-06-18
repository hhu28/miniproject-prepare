from flask import Flask, render_template, request, redirect, url_for
#from bokeh.util.string import encode_utf8
import requests
import json
import simplejson
import pandas as pd
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
    return 
#redirect(url_for('plot', name=name))
                            #cp = cp, acp=acp, op = op, aop=aop))
    #return render_template("input.html", name = name, cp = cp, acp=acp, op = op, aop=aop)
    
@app.route('/plot')
def plot():
    name = request.args.get('name')
    cp = request.args.get('cp')
    acp = request.args.get('acp')
    op = request.args.get('op')
    aop = request.args.get('aop')
    
    if name == None:
        name = 'fb'
    return 
#render_template("plot.html", name=name, cp = cp, acp=acp, op = op, aop=aop)




#@app.route('/show', methods=['GET'])
#def show():
#  return render_template('index.html', name = request.args.get('name'))




  #render_template('index.html')
  #getinput()
  #extractData()
  #return redirect('/index')
  #getinput()
  #extractData()
  #if request.method == 'POST':
    #name = request.form['name']
    #print 'name is:', name

    #flash('Success' + name)
    
    #return 
  #html = render_template('index.html')

  #return render_template('index.html', form=form)

#@app.route('/index')
#def index():
#  return render_template('index.html') 
  
if __name__ == '__main__':
  #app.debug(True)
  app.run(port=33507, host='0.0.0.0')