from flask import Flask, render_template, request
import pandas as pd
import csv
import os
import time
from initialization import *
from fitness import *
from crossover import *
from subprocess import call
st = time.time()

def call_genetic():
    call(['python','GeneticAlgo.py'])

app = Flask(__name__)
@app.route('/', methods = ['GET','POST'])
def index():
    return render_template('display.html')

@app.route('/data', methods = ['GET','POST'])
def data():
    if request.method == 'POST':
        f1 = request.files['courses']
        f1.save(f1.filename)
        f2 = request.files['faculty']
        f2.save(f2.filename)
    call_genetic()
    with open('Year1.csv', newline='') as f:
        reader = csv.DictReader(f)
        data1 = [row for row in reader]   
    with open('Year2.csv', newline='') as f:
        reader = csv.DictReader(f)
        data2 = [row for row in reader]    
    with open('Year3.csv', newline='') as f:
        reader = csv.DictReader(f)
        data3 = [row for row in reader]    
    with open('Year4.csv', newline='') as f:
        reader = csv.DictReader(f)
        data4 = [row for row in reader]        

# Create a list of headers

    header = list(data1[0].keys())



# Render the template with the data and headers
    return render_template('table.html', data1=data1,headers=header,data2=data2,data3=data3,data4=data4)
 

if __name__=="__main__":
    app.run(debug=True)
