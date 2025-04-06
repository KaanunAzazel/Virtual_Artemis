from fastapi import FastAPI
from models import TagRequest, LiveData
from scraper import scrape_by_tags
from typing import List

app = FastAPI(
    title="VTuberBR Data Scraper API",
    description="Microserviço para buscar lives de VTubers brasileiros com base em tags personalizadas da Twitch.",
    version="0.0.1"
)


@app.post("/scrape", response_model=List[LiveData])
async def scrape_lives(tag_request: TagRequest):
    return await scrape_by_tags(tag_request.tags)
