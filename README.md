# TWITTER-SCRAPPING
TWITTER SCRAPPING:
    This project aims to scrape Twitter data using the snscrape library, store it in MongoDB, and display the scraped data in a GUI built with Streamlit. The user can enter a keyword or hashtag to search, select a date range, and limit the number of tweets to scrape. The scraped data is displayed in the GUI and can be uploaded to nosql database, downloaded as a CSV or JSON file.

Requirments for this project:

Python 3.8 or higher
Snscrape
Pymongo
Pandas
Streamlit
Datetime


DEMO:A demo video of the working model is available on  Linkedin.

  


WORKFLOW:

Step 0: pip install all needed libraries.

Step 1: Importing all libraries.

from datetime import date
import pandas as pd
import snscrape.modules.twitter as sntwitter
import streamlit as st
import pymongo

Step 2: Getting input from user on streamlit sidebar


st.sidebar.header("**:blue[Give inputs here:point_down:]**")
keyword=st.sidebar.text_input("Enter hashtag/keyword of the tweet ")
limit=st.sidebar.number_input("Enter the no.of tweets you want",min_value=1,max_value=5000,step=1)
st.sidebar.write(":orange[Enter the date range]")
start_date=st.sidebar.date_input("Start Date (YYYY-MM-DD) : ")
end_date=st.sidebar.date_input("End Date (YYYY-MM-DD) : ")
current_date=str(date.today())

Step 3: Using snscrape and pandas,Tweets get scraped,converted into Dataframe and displayed in tabular format.

tweets = []
    # Using for loop, TwitterSearchScraper and enumerate function to scrape data and append tweets to list
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f"{keyword} since:{start_date} until:{end_date}").get_items()):
        if i >= limit:
            break
        tweets.append([tweet.id,tweet.user.username,
                            tweet.lang,tweet.date,
                            tweet.url,tweet.replyCount,tweet.retweetCount,
                            tweet.likeCount,tweet.rawContent,
                            tweet.source
                           ])
#converting the scrapped data into a dataframe
df=pd.DataFrame(tweets,columns=['user_id','user_name','language','datetime',
                               'url', 'reply_count','retweet_count',      'like_count', 
                              'tweet_content','source'])
if df.empty:
    st.subheader("**:point_left:Scraped tweets will visible after entering hashtag or keywords**")
else:
    st.success(f"**:blue[{keyword} _tweets]:thumbsup:**")
    st.write(df)

    st.write(":blue[select options below]")
    
    
# DataFrame to JSON file
def json_file(data):
    return data.to_json(orient='index')

# DataFrame to CSV file
def csv_file(data):
    return data.to_csv().encode('utf-8')


# Creating objects for dataframe and file conversion
csv =csv_file(df)
json = json_file(df)



           
Step 4: Streamlit is used to create GUI Buttons for Uploading and Downloading scraped tweets.


b1,b2,b3=st.columns(3)#CREATING BUTTONS HORIZONTALLY

#FIRST BUTTON FOR UPLOADING IN A MONGODB FILE
if b1.button("upload to mongodb"):
      try:
            # Note: Change the API into your Mongodb compass API, to avoid access restriction error. Here I have connected to my localhost connection.

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
           




To run the app, Navigate to the folder which app is present using CLI and run the command

streamlit run tweets.py


Future Improvements

*Expand the project to scrape data from other social media platforms
*Add authentication to the GUI to ensure data privacy
 List of available Hashtags present in database
 
The project code follows the PEP 8 coding standards with detailed information on the project's workflow and execution.
