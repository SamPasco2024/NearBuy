from flask import Flask, request, redirect, url_for, render_template, session
# Importing flask module in the project

#from flask_ngrok import run_with_ngrok
import requests
import json
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

app = Flask(__name__)
#run_with_ngrok(app)


@app.route("/", methods = ["GET", "POST"])
def store_search():
    
    if request.method == "POST":
        search_term = request.form["brand"]
        zipcode = request.form["zip_code"]
        
        name_to_search = search_term.lower().replace(" ", "_")
        zipcode_to_search = str(zipcode)
        
        best_match = process.extractOne(name_to_search, brand_names)[0]
        best_zip = process.extractOne(zipcode_to_search, zips)[0]
        
        print("\n\n\n *****SUBMIT REQUEST***** \n\n\n")
        print(megabase.columns)
        print(best_match, best_zip)

        
        filtered = megabase[
            (megabase['search_term_raw'] == str(best_match)) &
            (megabase['zipcode'] == int(best_zip)) &
            (megabase['search_engine'] == 'store_locator')
        ]

        data_display_dict = filtered.to_dict(orient='records') 
        print("MAIN:", filtered)
        
        
        

        filtered_ddd = megabase[
            (megabase['search_term_raw'] == str(best_match)) &
            (megabase['zipcode'] == int(best_zip)) &
            (megabase['page_rank'] == int(1))
        ]
        data_display_dict_ddd = filtered_ddd.to_dict(orient='records')
        print('AD:', filtered_ddd)


        #filt_stores = ulla_johnson[filt].to_dict(orient='records')

        return render_template('bw_results.html', results=data_display_dict, brand=best_match, 
                               zipp=best_zip, top_results = data_display_dict_ddd)
    else:
        return render_template('homepage.html')

    
###############
###Redirects, hello, basic Ulla

@app.route('/admin')
def admin():
    return redirect("https://www.espn.com/")

@app.route('/html')
def html():
    return render_template("htmltest.html")

@app.route('/hello/<name>')
def hello_name(name):
    return 'Hello %s!' % name

@app.route("/datahead/<n>")
def data_sample(n):
    df = megabase
    print(df)
    results = df.head(int(n)).to_dict(orient='records')
    return render_template('bw_results.html', results=results)
###############


###############

#Extra Code:
"""
@app.route('/meta', methods = ["GET", "POST"])
def meta_search():
    
    if request.method == "POST":
        rank = int(request.form["rank"])
        zip_code = int(request.form["zipcode"])
        print(rank, zip_code)
        rank_filt = le_specs_df['RankNumber'] <= rank
        zip_filt = le_specs_df['ZipCode'] == zip_code
        print(zip_filt)
        filt_results = le_specs_df[rank_filt & zip_filt].to_dict(orient='records')
        print(filt_results)
        return render_template('meta.html', results=filt_results)
    
    else:
        return render_template('meta.html')



### Homepage:
@app.route("/")
def hello():
    print("**********Printing in terminal - new visit**********")
    if request.method == "POST":
        brand = request.form["brand"]
        zipcode = request.form["zip_code"]
        
        print(brand, zipcode)
        
    return render_template("homepage.html")


@app.route('/results', methods = ["GET", "POST"])
def meta_search():
    
    if request.method == "POST":
        brand = session['brand']
        zipcode = session['zipcode']
        print("Inputted value from homepage", brand, zipcode)
        
        

        rank_filt = le_specs_df['RankNumber'] <= rank
        zip_filt = le_specs_df['ZipCode'] == zip_code
        
        
        print(zip_filt)
        filt_results = le_specs_df[rank_filt & zip_filt].to_dict(orient='records')
        print(filt_results)
        
        return render_template('meta.html')#, results=filt_results)
    
    else:
        return render_template('bw_results.html')
        
#From GPT

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def hello():
    print("New user")
    return "Hello world!"

@app.route("/greet", methods=["GET", "POST"])
def greet():
    if request.method == "POST":
        data = request.get_json()
        name = data["name"]
        message = f"Hello, {name}!"
        return jsonify({"message": message})
    else:
        return "Hello world!"


if __name__ == "__main__":
    app.run(debug=True)
"""


###############
if __name__ == "__main__":
    megabase = pd.read_csv('megabase.csv')
    brand_names = ['roc skincare', 'ulla johnson',
                   'hurley clothing', 'le specs',
                   'jl audio', 'obey clothing', 
                   'mark cross']
    zips = [
        '94110', '90210', '10001', '20001', '98101',
        '60601', '77002', '30303', '02108', '33131',
        '80202', '92101', '85004', '98104', '75201',
        '60611', '75205', '19104', '30363', '98109'
    ]
    
    app.run(debug=True)
    
    
    
    