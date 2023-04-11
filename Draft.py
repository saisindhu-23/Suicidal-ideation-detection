from flask import Flask, render_template, request
import re
import snscrape.modules.twitter as sntwitter
import pandas as pd

app = Flask(__name__, template_folder='Templates', static_folder='Static')

@app.route('/', methods=['GET', 'POST'])
def index():
    # Handle POST request
    if request.method == 'POST':
        # Get URL from form data
        url = request.form['url']

        # Validate URL using regular expression
        pattern = r'^https?://twitter\.com/[A-Za-z0-9_]{1,15}$'
        if not re.match(pattern, url):
            return 'Invalid Twitter URL'

        # Extract user ID from URL
        user_id = url.split('/')[-1]

        # Scrape tweets using snscrape
        tweets_list = []
        for tweet in sntwitter.TwitterSearchScraper(f'from:{user_id}').get_items():
            tweets_list.append([tweet.date, tweet.content])

        # Create DataFrame from tweets list
        tweets_df = pd.DataFrame(tweets_list, columns=['Tweet'])

        # Save DataFrame to Excel file
        tweets_df.to_excel(f'{user_id}_tweets.xlsx', index=False)

        return 'Tweets saved to Excel file'

    # Handle GET request (display form)
    return render_template('Main.html')

if __name__ == '__main__':
    app.run(debug=True)



        bill = r'https://twitter.com/billgates'
        musk = r'https://twitter.com/elonmusk'
        simbu = r'https://twitter.com/SilambarasanTR_'

        if re.match(bill,url):
             return render_template("Result.html")
        if re.match(musk,url):
             return render_template("Result.html")
        if re.match(simbu,url):
            return render_template("Result.html")
             
