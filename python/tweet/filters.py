import datetime as date

class Filters:
    use_limit = False
    max_tweets = 0
    query_search = ""
    by_username = ""
    use_date = False
    date_since = date.datetime(2000, 1, 1)
    date_until = date.datetime.now()
    top_tweets = False
    use_place = False
    place = "" #"Berlin, Germany"
    area = "" #"50km"
    use_geoLocales = False
    geo = "" #"55.75, 37.61"
