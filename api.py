from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from scraper import list_scrapers, run_scrape

class Item(BaseModel):
    scraper_name: str
    url: str

app = FastAPI()

@app.get("/api/v1/scrapers")
async def get_scrapers():
    """
    Endpoint to list all available scrapers.
    """
    return list_scrapers()

#TODO: take request from real user agent and add it / use it

@app.post('/api/v1/exec_scrape')
async def exec_scrape(item: Item):
    """
    Endpoint to execute the scraping for a given scraper and URL.
    """
    try:
        result = await run_scrape(item.scraper_name, item.url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

# todo: add update all products once hooked to db, 
