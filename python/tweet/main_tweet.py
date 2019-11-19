import GetOldTweets3 as got
import filters
import datetime

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
            tweetCriteria.setSince(fil.date_since.strftime("%Y-%m-%d"))
            tweetCriteria.setUntil(fil.date_until.strftime("%Y-%m-%d"))

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
        ultimo = None
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
            ultimo = tweet
        
        if ultimo is None:
            print("Retorno vazio")
            if conseguiu :
                fil.date_until = fil.date_until - datetime.timedelta(days=1)
                return Tweets._searchTweets(fil)
            return obj
        if ultimo.date.year != fil.date_since.year or ultimo.date.month != fil.date_since.month or ultimo.date.day != fil.date_since.day:
            print("Deu errado a busca, irá fazer novamente")
            print(ultimo.date.strftime("%d/%m/%y"))
            print(fil.date_since.strftime("%d/%m/%y"))
            fil.date_until = ultimo.date
            obj += Tweets._searchTweets(fil)
			
        return obj
        
        