from pydantic import BaseModel

class Artist:
    def __init__(self, id: str, name: str, thumbnailUrl: str | None = None):
        self.id = id
        self.name = name
        self.thumbnailUrl = thumbnailUrl

class Song:
    def __init__(self, id: str, title: str, artists: list[Artist], isExplicit: bool, streams: str, thumbnailUrl: str | None = None):
        self.id = id
        self.title = title
        self.artists = artists
        self.isExplicit = isExplicit
        self.streams = streams
        self.thumbnailUrl = thumbnailUrl

class Album:
    def __init__(self, id: str, title: str, year: str, artists: list[Artist], isExplicit: bool, thumbnailUrl: str | None = None):
        self.id = id
        self.title = title
        self.year = year
        self.artists = artists
        self.isExplicit = isExplicit
        self.thumbnailUrl = thumbnailUrl

class Podcast:
    def __init__(self, id: str, title: str, thumbnailUrl: str | None):
        self.id = id
        self.title = title
        self.thumbnailUrl = thumbnailUrl

class SearchData(BaseModel):
    query: str
