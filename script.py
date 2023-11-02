# Imports
import requests
import pandas as pd
from wordcloud import WordCloud
from textblob import TextBlob
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("Agg")
from flask import Flask, render_template, request
import creds
# import config

app = Flask(__name__)

# Setting the style for graphs
#plt.style.use(['dark_background', 'seaborn-muted', 'seaborn-poster'])
sns.set_style("darkgrid")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:

        # Get the user's query from the form
        user_query = request.form['query']

        twitter_data = []  

        payload = {
            'api_key': creds.api_key,
            'query': user_query,  
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

        # Create a list of all the snippets for word cloud generation
        all_snippets = " ".join(df['snippet'])

        # Create a WordCloud object
        wordcloud = WordCloud(width=800, height=400, background_color='black').generate(all_snippets)

        # Save the word cloud as an image file
        wordcloud.to_file('static/wordcloud.png')

        return render_template('result.html')
        
    except Exception as e:
        return render_template('handle.html')

if __name__ == '__main__':
    app.run(debug=True)