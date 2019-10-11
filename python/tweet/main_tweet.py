import GetOldTweets3 as got
import filters
from datetime import datetime

class Tweets:

    @staticmethod
    def _searchTweets(fil):
        tweetCriteria = got.manager.TweetCriteria()
        
        if fil.query_search != "" :
            x = fil.query_search
            tweetCriteria.setQuerySearch(x)                                           

        if fil.use_limit:
            x = fil.max_tweets
            tweetCriteria.setMaxTweets(x)
        
        if fil.by_username != "" :
            x = fil.by_username
            tweetCriteria.setUsername(x)

        if fil.top_tweets :
            tweetCriteria.setTopTweets(True)

        if fil.use_date :
            x = fil.date_since.strftime("%yyyy-%mm%dd")
            tweetCriteria.setSince(x)
            x = fil.date_until.strftime("%yyyy-%mm%dd")
            tweetCriteria.setUntil(x)

        if fil.use_place :
            x = fil.use_place
            tweetCriteria.setNear(x)
            x = fil.area
            tweetCriteria.setWithin(x)

        if fil.use_geoLocales == True :
            x = fil.geo
            tweetCriteria.setNear(x)
            

        obj = []
        conseguiu = False
        imp = []
        consegue = 5
        while conseguiu == False and consegue > 0:
            try:
                imp = got.manager.TweetManager.getTweets(tweetCriteria)
                conseguiu = True
                consegue = 5
            except:
                consegue = consegue -1
                conseguiu = False
        
        for tweet in imp:
            ob = {
						"ID" : tweet.id,
						"PERMALINK" : tweet.permalink,
						"USERNAME" : tweet.username,
						"TEXT" : tweet.text,
						"DATE" : tweet.date.strftime("%d/%m/%y"),
						"RETWEETS" : tweet.retweets,
						"FAVORITES" : tweet.favorites,
						"MENTIONS" : tweet.mentions,
						"HASHTAGS" : tweet.hashtags,
						"GEO" : tweet.geo
				  }
            obj.append(ob)
        return obj
        
        