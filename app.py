import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout='wide', page_title='Narendra Modi -Twitter Analysis')

st.header('Narendra Modi -Twitter Analysis')
st.subheader('KAVUCIKA P')  

@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/skathirmani/datasets/refs/heads/main/narendramodi_tweets.csv'
    data = pd.read_csv(url)
   
    data['Date'] = pd.to_datetime(data['created_at'])
    data['Year'] = data['Date'].dt.year
    data['Month'] = data['Date'].dt.to_period('M')
    return data

data = load_data()

st.write("Here is the Narendra Modi - Twitter Analysis:")
st.dataframe(data)

st.write("Column names in the DataFrame:", data.columns)

st.sidebar.header('Filter Tweets')

year_filter = st.sidebar.selectbox('Select Year', options=data['Year'].unique())

source_filter = st.sidebar.multiselect('Select Source', options=data['source'].unique())

filtered_data = data[(data['Year'] == year_filter) & (data['source'].isin(source_filter))]

if filtered_data.empty:
    st.warning('No data available for the selected Year and Source combination.')
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label='Number of Tweets', value=len(filtered_data))
    with col2:
        avg_retweets = filtered_data['retweets_count'].mean()
        st.metric(label='Average Retweets', value=f"{avg_retweets:.2f}")
    with col3:
        avg_likes = filtered_data['favorite_count'].mean()
        st.metric(label='Average Likes', value=f"{avg_likes:.2f}")

    st.header('Month-wise Tweet Count')
    month_wise_tweet_count = filtered_data.groupby(filtered_data['Month'].astype(str)).size().reset_index(name='TweetCount')

    fig = px.line(month_wise_tweet_count, x='Month', y='TweetCount', title='Month-wise Tweet Count')
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.header('Month-wise Hashtag Count')
    
        month_wise_hashtag_count = filtered_data.groupby(filtered_data['Month'].astype(str))['hashtags_count'].sum().reset_index()

        fig = px.bar(month_wise_hashtag_count, x='Month', y='hashtags_count', title='Month-wise Hashtag Count')
        st.plotly_chart(fig)

    with col2:
        st.header('Top 10 Tweets by Likes')
        top_10_tweets = filtered_data[['text', 'favorite_count']].sort_values(by='favorite_count', ascending=False).head(10)
        st.table(top_10_tweets[['text','favorite_count']])

from textblob import TextBlob
def get_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'
filtered_data['Sentiment'] = filtered_data['text'].apply(get_sentiment)
st.header('Sentiment Analysis')
sentiment_counts = filtered_data['Sentiment'].value_counts()
fig = px.pie(names=sentiment_counts.index, values=sentiment_counts.values, title='Sentiment Distribution')
st.plotly_chart(fig)
