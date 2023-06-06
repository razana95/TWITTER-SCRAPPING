# TWITTER-SCRAPPING
I have written two codes and attached both the files with the name mytwitt.py and new.py. my.twitt.py is a basic code to use streamlit and in new.py i have added some more options and image.


### TWITTER SCRAPPING:
    This project aims to scrape Twitter data using the snscrape library, store it in MongoDB, and display the scraped data in a GUI built with Streamlit. The user can enter a keyword or hashtag to search, select a date range, and limit the number of tweets to scrape. The scraped data is displayed in the GUI and can be uploaded to nosql database, downloaded as a CSV or JSON file.

Requirments for this project:

Python 3.8 or higher
Snscrape
Pymongo
Pandas
Streamlit
Datetime


DEMO:A demo video of the working model is available on  Linkedin-https://www.linkedin.com/in/hasna-razhana-473733271/

  
CODE:1[MYTWITT.PY]

### WORKFLOW:

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
    #Using for loop, TwitterSearchScraper and enumerate function to scrape data and append tweets to list
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
    
    
#DataFrame to JSON file
def json_file(data):
    return data.to_json(orient='index')

#DataFrame to CSV file
def csv_file(data):
    return data.to_csv().encode('utf-8')


### Creating objects for dataframe and file conversion
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
      
      
 
 CODE:2[new.py)
(giving some more options and added image)


#step:1--importing needed libraries
import snscrape.modules.twitter as sntwitter
import streamlit as st
import pandas as pd
import pymongo
#from pymongo import MongoClient
#from PIL import Image
from datetime import date
import json
from PIL import Image#for adding image



#step:2: main function starts here and given some option using selectbox.
def main():
 #create lit to append the scrapped tweets
  tweets = []
    #establishing mongodb connection 
  client=pymongo.MongoClient("localhost",27017)
  db=client.my_database
  collection=db.twitter_data
  
  st.title("Twitter Scraping")

#step:3--adding selectbox and giving 4 options in menu.
    
  menu = ["Home","About","Search","Download"]
  choice = st.sidebar.selectbox("Menu",menu)

  #Menu 1 is Home page 
  if choice=="Home":
    st.write('''This app is a Twitter Scraping web app created using Streamlit. 
             It scrapes the twitter data for the given hashtag/ keyword for the given period.
             The tweets are uploaded in MongoDB and can be dowloaded as CSV or a JSON file.''')
    image=Image.open("imagetwitt.jpeg")#adding image
    st.image(image)
  #Menu 2 is about the Twitter Scrape libraries, databases and apps
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

  #Menu 3 is a search option
  elif choice=="Search":
    #Every time after the last tweet the database will be cleared for updating new scraping data
    #collection.delete_many({})

    #step:4--Form for collecting user input for twitter scrape
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
    
#step:5--calling main function   
main()



           




To run the app, Navigate to the folder which app is present using CLI and run the command

streamlit run tweets.py


Future Improvements

*Expand the project to scrape data from other social media platforms
*Add authentication to the GUI to ensure data privacy
 List of available Hashtags present in database
 
The project code follows the PEP 8 coding standards with detailed information on the project's workflow and execution.
