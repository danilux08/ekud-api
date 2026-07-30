from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from ytmusicapi import YTMusic
from .models import SearchData

app = FastAPI()
ytmusic = YTMusic()

@app.get("/", response_class=HTMLResponse)
async def test():
    return "<h1>Hello, World!</h1>"

@app.post("/search")
async def search(data: SearchData):
    return ytmusic.search(f"{data.query}")
