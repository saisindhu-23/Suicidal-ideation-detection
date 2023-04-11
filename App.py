from flask import Flask, render_template, request
import re
import snscrape.modules.twitter as sntwitter
import pandas as pd
import firebase_admin
from firebase_admin import credentials
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin
import subprocess

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__, template_folder='Templates', static_folder='Static')
CORS(app, support_credentials=True)
api = Api(app)

class AddToDoItem(Resource):
            @app.route('/addItem', methods=['GET','POST'])
            @cross_origin(support_credentials=True)

            def addItem():
                todo = {"url": url}
                try:
                    json_data = request.get_json(force=True)
                    itemValue = todo.addTodoItem(json_data)
                    return jsonify(itemValue)
                except Exception as ex:
                     return str(ex), 400

class GetTodoItem(Resource):
    @app.route('/getItem', methods=['POST'])
    @cross_origin(support_credentials=True)
    def getItem():
        todo = {"url": url,
                "result": "Non - suicidal"}
        try:
            json_data = request.get_json(force=True)
            itemId = json_data['id']
            itemValue = todo.getTodoItem(itemId)
            return jsonify(itemValue)
        except Exception as ex:
            return str(ex), 400  

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':

        url = request.form['url']

        pattern = r'^https?://twitter\.com/[A-Za-z0-9_]{1,15}$'
        if not re.match(pattern, url):
            return render_template("Invalid.html")
        
        user_id = url.split('/')[-1]

        tweets_list = []
        for tweet in sntwitter.TwitterSearchScraper(f'from:{user_id}').get_items():
            tweets_list.append([tweet.content])

        tweets_df = pd.DataFrame(tweets_list, columns=['Tweet'])

        tweets_df.to_excel(f'./Data/Input_tweets.xlsx', index=False)

        render_template("Processing.html")

        return subprocess.run(["python", "lstm.py"])

    return render_template('Main.html')           

if __name__ == '__main__':
    app.run(debug=True)