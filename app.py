import pandas as pd
import streamlit as st
import plotly.express as px

#name of the web page
st.set_page_config(layout='wide', page_title='Narendra Modi -Twitter Analysis')

# 1.Write a header "Narendra Modi - Twitter Analysis". Make sure to add your name below it

st.header('Narendra Modi -Twitter Analysis')
st.subheader('KAVUCIKA P')  

# Loading the data
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/skathirmani/datasets/refs/heads/main/narendramodi_tweets.csv'
    data = pd.read_csv(url)

    # Converts the 'created_at' column from string format to a proper datetime format
    data['Date'] = pd.to_datetime(data['created_at'])
    # Extracts the year from the 'Date' column
    data['Year'] = data['Date'].dt.year
    # Extracts the month (year + month) from the 'Date' column
    data['Month'] = data['Date'].dt.to_period('M')
    return data

data = load_data()

# displaying the dataframe to see what are in the given url
st.write("Here is the Narendra Modi - Twitter Analysis:")
st.dataframe(data)

#doing this step to ensure that the column names we give is correctly matched with the column name in the data frame
st.write("Column names in the DataFrame:", data.columns)

# 2.Sidebar Filters : Year filter and Source filter
st.sidebar.header('Filter Tweets')

# Year filter
year_filter = st.sidebar.selectbox('Select Year', options=data['Year'].unique())

# Source filter
source_filter = st.sidebar.multiselect('Select Source', options=data['source'].unique())

# Filter the data based on year and source
filtered_data = data[(data['Year'] == year_filter) & (data['source'].isin(source_filter))]

if filtered_data.empty:
    st.warning('No data available for the selected Year and Source combination.')
else:

    # 3.First row, three metrics using three columns: No. of Tweets , Average Retweets , Average Likes
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label='Number of Tweets', value=len(filtered_data))

    with col2:
        avg_retweets = filtered_data['retweets_count'].mean()
        st.metric(label='Average Retweets', value=f"{avg_retweets:.2f}")

    with col3:
        avg_likes = filtered_data['favorite_count'].mean()
        st.metric(label='Average Likes', value=f"{avg_likes:.2f}")

    # 4.Second row (full row chart) - Line chart to display month-wise total number of tweets
    st.header('Month-wise Tweet Count')
    month_wise_tweet_count = filtered_data.groupby(filtered_data['Month'].astype(str)).size().reset_index(name='TweetCount')

    # Line chart
    fig = px.line(month_wise_tweet_count, x='Month', y='TweetCount', title='Month-wise Tweet Count')
    st.plotly_chart(fig, use_container_width=True)

    # 5.Third row (Two columns) - Month-wise total number of hashtags using bar chart , Table to display Top 10 tweets (use text column)  based on number of likes
    # Third row with two columns
    col1, col2 = st.columns(2)

    # Column 1: Bar chart for month-wise hashtag count
    with col1:
        st.header('Month-wise Hashtag Count')
    
        # Counting hashtags based on the 'hashtags_count' column
        month_wise_hashtag_count = filtered_data.groupby(filtered_data['Month'].astype(str))['hashtags_count'].sum().reset_index()

        # Bar chart
        fig = px.bar(month_wise_hashtag_count, x='Month', y='hashtags_count', title='Month-wise Hashtag Count')
        st.plotly_chart(fig)

    # Column 2: Table for top 10 tweets by likes
    with col2:
        st.header('Top 10 Tweets by Likes')
        # Sorting tweets by likes
        top_10_tweets = filtered_data[['text', 'favorite_count']].sort_values(by='favorite_count', ascending=False).head(10)
        st.table(top_10_tweets[['text']])

    # 6.Optional: Create a new tab called “Hashtag analysis” , Identify all hashtags used in the text column, and visualize top 10 hashtags based on frequency
    if st.checkbox('Show Hashtag Analysis'):
        st.header('Hashtag Analysis')

        # Counting top 10 hashtags based on the 'hashtags_count' column
        top_hashtags = filtered_data[['text', 'hashtags_count']].groupby('hashtags_count').size().reset_index(name='Count')

        # We want the top 10 hashtags based on their count
        top_hashtags = top_hashtags.sort_values(by='Count', ascending=False).head(10)

        # Displaying the results
        st.table(top_hashtags)

        # Bar chart for top hashtags based on counts
        fig = px.bar(top_hashtags, x='hashtags_count', y='Count', title='Top 10 Hashtags Count')
        st.plotly_chart(fig)

