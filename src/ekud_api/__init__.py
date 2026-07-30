from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from ytmusicapi import YTMusic
from .models import SearchData
from .player import get_player_html

app = FastAPI()
ytmusic = YTMusic()

@app.get("/player/{videoId}", response_class=HTMLResponse)
async def test(videoId: str):
    return get_player_html(videoId)

@app.post("/search")
async def search(data: SearchData):
    return ytmusic.search(f"{data.query}")
