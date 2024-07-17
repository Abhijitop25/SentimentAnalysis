from django.shortcuts import render
from googleapiclient.discovery import build
from textblob import TextBlob
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import urllib.parse

def get_comments(video_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100
    )
    response = request.execute()

    comments = []
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comments.append(comment)
    
    return comments

def analyze_sentiment(comments):
    positive_comments, negative_comments, neutral_comments = [], [], []

    for comment in comments:
        analysis = TextBlob(comment)
        if analysis.sentiment.polarity > 0:
            positive_comments.append(comment)
        elif analysis.sentiment.polarity < 0:
            negative_comments.append(comment)
        else:
            neutral_comments.append(comment)

    return positive_comments, negative_comments, neutral_comments

def plot_sentiment(positive, negative, neutral):
    labels = ['Positive', 'Negative', 'Neutral']
    sizes = [len(positive), len(negative), len(neutral)]
    colors = ['#ff9999','#66b3ff','#99ff99']
    explode = (0.1, 0, 0)  

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)

    return uri

def youtube_sentiment(request):
    if request.method == 'POST':
        video_url = request.POST['video_url']
        video_id = video_url.split('v=')[1]
        api_key = 'AIzaSyBbSxeUIoYmbYqajqEYr7s2BvqsJRACVWk'

        comments = get_comments(video_id, api_key)
        positive, negative, neutral = analyze_sentiment(comments)

        # Limiting to 3 comments for each sentiment category
        positive_comments = positive[:3]
        negative_comments = negative[:3]
        neutral_comments = neutral[:3]

        sentiment_plot = plot_sentiment(positive, negative, neutral)

        context = {
            'positive': len(positive),
            'negative': len(negative),
            'neutral': len(neutral),
            'sentiment_plot': sentiment_plot,
            'positive_comments': positive_comments,
            'negative_comments': negative_comments,
            'neutral_comments': neutral_comments,
        }
        return render(request, 'sentiment_analysis/Main.html', context)
    
    return render(request, 'sentiment_analysis/Main.html')
