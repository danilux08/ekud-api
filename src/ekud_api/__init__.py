from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from ytmusicapi import YTMusic
from .models import Artist, Song, Album, Podcast, SearchData
from .player import get_player_html

app = FastAPI()
ytmusic = YTMusic()

@app.get("/player/{videoId}", response_class=HTMLResponse)
async def videoPlayer(videoId: str):
    return get_player_html(videoId)

SEARCH_LIMIT = 50

@app.post("/search/artists")
async def searchArtists(data: SearchData):
    query = data.query
    results = ytmusic.search(query = f"{query}", limit = SEARCH_LIMIT, filter = "artists")
    artists = []
    try:
        for result in results:
            if result["category"] != "Artists" or result["resultType"] != "artist":
                continue
            thumbnailUrl = None
            try:
                thumbnailUrl = result["thumbnails"][1]["url"]
            except:
                pass
            artists.append(Artist(
                result["browseId"],
                result["artist"],
                thumbnailUrl
            ))
    except:
        print(f"Results of query {query} are invalid.")
    return artists

@app.post("/search/songs")
async def searchSongs(data: SearchData):
    query = data.query
    results = ytmusic.search(query = f"{query}", limit = SEARCH_LIMIT, filter = "songs")
    songs = []
    try:
        for result in results:
            if result["category"] != "Songs" or result["resultType"] != "song" or result["videoType"] != "MUSIC_VIDEO_TYPE_ATV":
                continue
            songArtists = []
            try:
                for songArtist in result["artists"]:
                    songArtists.append(Artist(
                        songArtist["id"],
                        songArtist["name"]
                    ))
            except:
                pass
            thumbnailUrl = None
            try:
                thumbnailUrl = result["thumbnails"][1]["url"]
            except:
                pass
            songs.append(Song(
                result["videoId"],
                result["title"],
                songArtists,
                result["isExplicit"],
                thumbnailUrl
            ))
    except:
        print(f"Results of query {query} are invalid.")
    return songs

@app.post("/search/albums")
async def searchAlbums(data: SearchData):
    query = data.query
    results = ytmusic.search(query = f"{query}", limit = SEARCH_LIMIT, filter = "albums")
    albums = []
    try:
        for result in results:
            if result["category"] != "Albums" or result["resultType"] != "album":
                continue
            albumArtists = []
            try:
                for albumArtist in result["artists"]:
                    albumArtists.append(Artist(
                        albumArtist["id"],
                        albumArtist["name"]
                    ))
            except:
                pass
            thumbnailUrl = None
            try:
                thumbnailUrl = result["thumbnails"][1]["url"]
            except:
                pass
            albums.append(Album(
                result["browseId"],
                result["title"],
                result["year"],
                albumArtists,
                result["isExplicit"],
                thumbnailUrl
            ))
    except:
        print(f"Results of query {query} are invalid.")
    return albums

@app.post("/search/podcasts")
async def searchPodcasts(data: SearchData):
    query = data.query
    results = ytmusic.search(query = f"{query}", limit = SEARCH_LIMIT, filter = "podcasts")
    podcasts = []
    try:
        for result in results:
            if result["category"] != "Podcasts" or result["resultType"] != "podcast":
                continue
            thumbnailUrl = None
            try:
                thumbnailUrl = result["thumbnails"][1]["url"]
            except:
                pass
            podcasts.append(Artist(
                result["browseId"],
                result["title"],
                thumbnailUrl
            ))
    except:
        print(f"Results of query {query} are invalid.")
    return podcasts
