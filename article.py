import json

class Article:
    def __init__(self, urlSite, header, paragraphs, lists, subtitles):
        self.urlSite = urlSite
        self.header = header
        self.paragraphs = paragraphs
        self.lists = lists
        self.subtitles = subtitles

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)