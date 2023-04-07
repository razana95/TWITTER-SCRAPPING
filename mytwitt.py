#IMPORTING NEEDED MODULES AND LIBRARIES
import pandas as pd
import snscrape.modules.twitter as sntwitter
import streamlit as st
from datetime import date
import pymongo

#SETTING UP PAGE CONFIGURATION(OPTIONAL)
st.set_page_config(layout="wide", page_title='Get_Tweets')#layout can be wide or centered

st.header(":green[WELCOME TO TWITTER SCRAPPING]")

#project decription
st.write(""" 
        This website helps you to Scrape Tweets using a **keyword or hashtag** , date range, 
        and total number of tweets needed. 
        **snscrape** is used for scraping the tweets and the 
        tweets get displayed in the GUI that built with **Streamlit** 
        and which can be uploaded into **MongoDB** database and downloaded 
        as a **CSV**,**JSON** file.""")


#SIDEBAR LAYOUT
st.sidebar.header("**:blue[Give inputs here:point_down:]**")
keyword=st.sidebar.text_input("Enter hashtag/keyword of the tweet ")
limit=st.sidebar.number_input("Enter the no.of tweets you want",min_value=1,max_value=5000,step=1)
st.sidebar.write(":orange[Enter the date range]")
start_date=st.sidebar.date_input("Start Date (YYYY-MM-DD) : ")
end_date=st.sidebar.date_input("End Date (YYYY-MM-DD) : ")
current_date=str(date.today())

#SCRAPING TWEETS AND APPENDING IT IN A LIST
tweets=[]
for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{keyword} since:{start_date} until:{end_date}').get_items()):
      if i > limit:
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

    st.write(":blue[select options below]")

#FUNCTION TO CONVERT AS A CSV FILE
def csv_file(data):
      return data.to_csv().encode("utf-8")

#FUNCTION TO CONVERT AS A JSON FILE
def json_file(data):
      return data.to_json(orient="index")

#CALLING FUNCTION
csv=csv_file(df)
json=json_file(df)
      

b1,b2,b3=st.columns(3)#CREATING BUTTONS HORIZONTALLY

#FIRST BUTTON FOR UPLOADING IN A MONGODB FILE
if b1.button("upload to mongodb"):
      try:
            client=pymongo.MongoClient("localhost",27017)
            db=client.my_database
            collection=db.twitter_data
            documents={"scrapped _word" : keyword,
                       "scrapped _date" : current_date,
                       "scrapped_data" : df.to_dict("records")
                      }  
            collection.delete_many({})
            collection.insert_one(documents)
            b1.success( "Successfully Uploaded in mongodb :thumbsup:" )
      except:
            st.error( ":red_circle: Something went wrong .Try again later")


#SECOND BUTTON TO DOWNLOAD AS A CSV FILE
if b2.download_button(label="Download as CSV",
                      data=csv,
                      file_name=f'{keyword}_tweets.csv',
                      mime='text/csv'
                     ):
      b2.success(" downloaded successfully :thumbsup:")
      

 #THIRD BUTTON TO DOWNLOAD AS A JSON FILE        
if b3.download_button(label="download as json",
                      data=json,
                      file_name= f'{keyword}_tweets.json',
                      mime= 'text/csv'
                      ):
      b2.success("Downloaded successfully :thumbsup:")
           

