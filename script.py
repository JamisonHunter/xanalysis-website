# Imports
import requests
import pandas as pd
from textblob import TextBlob
import seaborn as sns
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, jsonify
import creds

app = Flask(__name__)

# setting the style for seaborn graphs
plt.style.use(['dark_background', 'seaborn-muted', 'seaborn-poster'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # Get the user's query from the form
    user_query = request.form['query']

    twitter_data = []  

    # Replace 'user_query' with 'query' in the payload
    payload = {
       'api_key': creds.api_key,
       'query': user_query,  # Use the user's query here
       'num': '10'
    }
    response = requests.get(
        'https://api.scraperapi.com/structured/twitter/search', params=payload)
    data = response.json()

    title = []
    snippet = []
    sentiment_snippet = []
    sentiment_type = []

    for i in range(len(data["organic_results"])):
        blob = TextBlob(data["organic_results"][i]["snippet"])
        sentiment = blob.sentiment.polarity
        title.append(data["organic_results"][i]["title"])
        snippet.append(data["organic_results"][i]["snippet"])
        sentiment_snippet.append(sentiment)

        if sentiment == 0:
            sentiment_type.append("neutral")

        elif sentiment > 0:
            sentiment_type.append("positive")

        else:
            sentiment_type.append("negative")

    data_dict = {"title": title, 
                "snippet": snippet,
                "sentiment": sentiment_snippet,
                "sentiment_type": sentiment_type}


    df = pd.DataFrame(data_dict)

    fig = plt.figure()
    ax = df["sentiment_type"].value_counts().plot(kind="barh")
    ax.set_title(f"Sentiment Regarding {user_query.upper()}")

    plt.savefig("static/sentiment_graph.png")

    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)