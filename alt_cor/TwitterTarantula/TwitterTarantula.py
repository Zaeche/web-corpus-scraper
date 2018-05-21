# -*- coding: UTF-8 -*-
#############################################
# Author: Zeeshan Shahid                    #
# Last edited: 19-09-2016                   #
############################################

import tweepy
import sys, uuid, random, time
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

############### To self: fix for follower list retrieval error ########
# http://stackoverflow.com/questions/29332259/tweepy-tweeperror-rate-limit-exceeded
#######################################################################

##################### Setup below (do no change)#######################
# Get these from your Twitter account
access_token = ""
access_secret = ""
consumer_key = ""
consumer_secret = ""

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

################## Code below//Setup complete ###########################
HOME = "twitter"                         #where the heart is
BUILDINGS = 10                           #users/twits
LEGS = 16                                #user-timelines-pages
JOINTS = 200                             #user-tweets
# adds up to 3200 tweets per user, 16 pages * 200 tweets/page

class TwitterTarantula:
    def __init__(self, handle):
        self.handle = handle
        self.past = []                   #The places the tarantula's been, things seen--

    def Crawl(self):
        #Debug: rate limit checker
        """data = api.rate_limit_status()
        print data['resources']['statuses']['/statuses/home_timeline']
        print data['resources']['users']['/users/lookup']"""

        outname = "output__twitter__text.txt" #+ str(uuid.uuid4().hex) + ".txt"
        for rooms in range(0, BUILDINGS+1): #users and timelines
            try:
                self.past.append(self.handle)

                user_handles = []
                for follower in tweepy.Cursor(api.followers, id=self.handle).items():
                    user_handles.append(follower.screen_name.encode("utf-8"))
                user_handles = filter (None, user_handles)
                print user_handles

                #Returns a list of statuses--each page a list; Honours Twitter's pagination limit of 3200 tweets
                public_tweets = tweepy.Cursor(api.user_timeline, id=self.handle, count=JOINTS).pages(LEGS)
                for page in public_tweets:
                    for status in page:
                        with open(outname, "ab") as outfile:
                            outfile.write(status.text.encode("utf-8"))

                random.shuffle(user_handles)
                self.handle = random.choice(user_handles)
                print self.handle + "___DONE____"
                ## Add some sort of sleep/wait here - a request per minute perhaps - to avoid the RateLimit
                # time.sleep(60)

            except tweepy.RateLimitError:
                print sys.exc_info()[0], "\nRate limit exceeded. Waiting for the 15-minute block to pass ..."
                start = time.time()
                end = start + (15 * 60) #s
                while(start < end):
                    m, s = (end-start)/60, (end-start)%60
                    if s > 9:
                        sys.stdout.write('%s%d%s%d\r' % ("Time remaining: ", m, ":", s))
                    if s == 10:
                        sys.stdout.write('%s\r' % "\t\t\t\t")
                    else:
                        sys.stdout.write('%s%d%s%d\r' % ("Time remaining: ", m, ":", s))
                    start = time.time() # update

def main():
    theamazingvenom = TwitterTarantula(HOME)
    theamazingvenom.Crawl()
    return 0

if __name__ == '__main__':
    main()



""" ############ References and Miscellanea ################

    http://stackoverflow.com/questions/11351711/getting-a-users-entire-twitter-timeline-with-tweepy (including retweets option syntax)

    http://docs.tweepy.org/en/latest/api.html

    http://stackoverflow.com/questions/4897359/output-to-the-same-line-overwriting-previous-output-python-2-5
"""
