import GetOldTweets3 as got
import json

class File:
    
    def __init__(self, director):
        self.director = director

    def _writeOnFile(self, json_text):
        file = open(self.director,"w+")
        file.writelines(json_text)
        file.close()