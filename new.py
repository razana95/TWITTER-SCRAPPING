import snscrape.modules.twitter as sntwitter
import streamlit as st
import pandas as pd
import pymongo
#from pymongo import MongoClient
#from PIL import Image
from datetime import date
import json
from PIL import Image


#client=pymongo.MongoClient("localhost",27017)
#db=client.my_database
#collection=db.twitter_data
# Here starts the main function
def main():
  #count=0
  tweets = []
  client=pymongo.MongoClient("localhost",27017)
  db=client.my_database
  collection=db.twitter_data
  
  st.title("Twitter Scraping")
  menu = ["Home","About","Search","Download"]
  choice = st.sidebar.selectbox("Menu",menu)

  # Menu 1 is Home page 
  if choice=="Home":
    st.write('''This app is a Twitter Scraping web app created using Streamlit. 
             It scrapes the twitter data for the given hashtag/ keyword for the given period.
             The tweets are uploaded in MongoDB and can be dowloaded as CSV or a JSON file.''')
    image=Image.open("imagetwitt.jpeg")
    st.image(image)
  # Menu 2 is about the Twitter Scrape libraries, databases and apps
  elif choice=="About":
    # Info about Twitter Scrapper
    with st.expander("Twitter Scrapper"):
      st.write('''Twitter Scraper will scrape the data from Public Twitter profiles.
                    It will collect the data about **date, id, url, tweet content, users/tweeters,reply count, 
                    retweet count, language, source, like count, followers, friends** and lot more information 
                    to gather the real facts about the Tweets.''')

    # Info about Snscraper
    with st.expander("Snscraper"):
      st.write('''Snscrape is a scraper for social media services like *twitter, faceboook, instagram and so on*. 
                   It scrapes **user profiles, hashtages, other tweet information** and returns the discovered items from the relavent posts/tweets.''')

    # Info about MongoDB database
    with st.expander("Mongodb"):
      st.write('''MongoDB is an open source document database used for storing unstrcutured data. The data is stored as JSON like documents called BSON. 
                  It is used by developers to work esaily with real time data analystics, content management and lot of other web applications.''')

    # Info about Streamlit framework
    with st.expander("Streamlit"):
      st.write('''Streamlit is a **awesome opensource framwork used for buidling highly interactive sharable web applications*** in python language. 
                  Its easy to share *machine learning and datasciecne web apps* using streamlit.
                  It allows the app to load the large set of datas from web for manipulation and  performing expensive computations.''')

  # Menu 3 is a search option
  elif choice=="Search":
    # Every time after the last tweet the database will be cleared for updating new scraping data
    #collection.delete_many({})

    # Form for collecting user input for twitter scrape
    with st.form(key='form1'):
      # Hashtag input
      st.subheader(":green[Tweet searching Form]")
      keyword=st.text_input("Enter hashtag/keyword of the tweet ")
      limit=st.number_input("Enter the no.of tweets you want:max-limit is 1000",min_value=1,max_value=1000,step=10)

      # From date to end date for scraping
      st.write(":blue[Enter the date range]")
      start_date = st.date_input('Start date')
      end_date= st.date_input('End date')
      current_date=str(date.today())
      
      # Submit button to scrap
      submit_button = st.form_submit_button(label="submit")
    
    if submit_button:
      
      # TwitterSearchScraper will scrape the data and insert into MongoDB database
      for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{keyword} since:{start_date} until:{end_date}').get_items()):
        # To verify the limit if condition is set
        if i >= limit:
           break
        tweets.append([tweet.id,tweet.user.username,
                            tweet.lang,tweet.date,
                            tweet.url,tweet.replyCount,tweet.retweetCount,
                            tweet.likeCount,tweet.rawContent,
                            tweet.source
                           ])
      df=pd.DataFrame(tweets,columns=['user_id','user_name','language','datetime',
                               'url', 'reply_count','retweet_count', 'like_count', 
                              'tweet_content','source'])
      if df.empty:
        st.subheader("**:point_left:Scraped tweets will visible after entering hashtag or keywords**")
      else:
        st.success(f"**:blue[{keyword} _tweets]:thumbsup:**")
        st.write(df)

      #st.write(":blue[select options below]")
    if st.button("upload to mongodb"):
      try:
            df=pd.DataFrame(tweets,columns=['user_id','user_name','language','datetime',
                               'url', 'reply_count','retweet_count', 'like_count', 
                              'tweet_content','source'])
            #client=pymongo.MongoClient("localhost",27017)
            #db=client.my_database
            #collection=db.twitter_data
            documents={"scrapped _word" : keyword,
                       "scrapped _date" : current_date,
                       "scrapped_data" : df.to_dict()
                      }  
            #collection.delete_many({})
            collection.insert_one(documents)
            st.success( "Successfully Uploaded in mongodb :thumbsup:" )
      except pymongo.errors.PyMongoError:
            st.error( "Failed to upload to mongodb. Please Try again later")


  else:
    b1,b2,=st.columns(2)#CREATING BUTTONS HORIZONTALLY
    

    with b1:
      #st.write("Download the tweet data as CSV File")
      # save the documents in a dataframe
      df = pd.DataFrame(list(collection.find()))
      # Convert dataframe to csv
      #df.to_csv('twittercsv.csv')
      def convert_df(data):
        # Cache the conversion to prevent computation on every rerun
        return data.to_csv().encode('utf-8')
      csv = convert_df(df)
      if st.download_button(
                        label="Download data as CSV",
                        data=csv,
                        file_name='twtittercsv.csv',
                        mime='text/csv',
                        ):
        st.success("Successfully Downloaded:thumpsup:")

    # Download the scraped data as JSON
    with b2:
      #st.write("Download the tweet data as JSON File")
      # Convert dataframe to json string instead as json file 
      df = pd.DataFrame(list(collection.find()))
      twtjs = df.to_json(default_handler=str).encode()
      # Create Python object from JSON string data
      obj = json.loads(twtjs)
      js = json.dumps(obj, indent=4)
      if st.download_button(
                        label="Download data as JSON",
                        data=js,
                        file_name='twtjson.js',
                        mime='text/js',
                        ):
        st.success("Successfully Downloaded:thumpsup:")
main()


