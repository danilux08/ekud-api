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

@app.post("/search")
async def search(data: SearchData):
    query = data.query
    results = ytmusic.search(query = f"{query}", limit = 100)
    artists = []
    songs = []
    albums = []
    podcasts = []
    try:
        for result in results:
            # This check is temporary
            if result["category"] is not None:
                continue
            match result["resultType"]:
                case "artist":
                    artists.append(result)
                case "song":
                    if result["videoType"] is not "MUSIC_VIDEO_TYPE_ATV":
                        songs.append(result)
                case "album":
                    albums.append(result)
                case "podcast":
                    podcasts.append(result)
    except:
        print(f"Results of query {query} are invalid.")
    formattedArtists = []
    formattedSongs = []
    formattedAlbums = []
    formattedPodcasts = []
    for artist in artists:
        thumbnailUrl = None
        try:
            thumbnailUrl = artist["thumbnails"][1]["url"]
        except:
            pass
        formattedArtists.append(Artist(
            artist["browseId"],
            artist["artist"],
            thumbnailUrl
        ))
    for song in songs:
        thumbnailUrl = None
        try:
            thumbnailUrl = song["thumbnails"][1]["url"]
        except:
            pass
        songArtists = []
        try:
            for songArtist in song["artists"]:
                artistId = songArtist["id"]
                if artistId is None:
                    continue
                songArtists.append(Artist(
                    artistId,
                    songArtist["name"]
                ))
        except:
            pass
        formattedSongs.append(Song(
            song["videoId"],
            song["title"],
            songArtists,
            song["isExplicit"],
            song["views"],
            thumbnailUrl
        ))
    for album in albums:
        thumbnailUrl = None
        try:
            thumbnailUrl = album["thumbnails"][1]["url"]
        except:
            pass
        albumArtists = []
        try:
            for albumArtist in album["artists"]:
                artistId = albumArtist["id"]
                if artistId is None:
                    continue
                albumArtists.append(Artist(
                    artistId,
                    albumArtist["name"]
                ))
        except:
            pass
        formattedAlbums.append(Album(
            album["browseId"],
            album["title"],
            album["year"],
            albumArtists,
            album["isExplicit"],
            thumbnailUrl
        ))
    for podcast in podcasts:
        thumbnailUrl = None
        try:
            thumbnailUrl = podcast["thumbnails"][1]["url"]
        except:
            pass
        formattedPodcasts.append(Podcast(
            podcast["browseId"],
            podcast["title"],
            thumbnailUrl
        ))
    return {
        "artists": formattedArtists,
        "songs": formattedSongs,
        "albums": formattedAlbums,
        "podcasts": formattedPodcasts
    }
