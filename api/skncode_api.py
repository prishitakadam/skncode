from fastapi import FastAPI
from playwright.sync_api import sync_playwright
from fastapi.middleware.cors import CORSMiddleware

import sys
sys.path.append('../')

from scrapper.scrapper_playwright import Scrapper

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "127.0.0.1/",
    "127.0.0.1:8000/",
    "chrome-extension://kgcbpbieeopdolioidlimmdioleomejd",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def ingredient(url: str):
    with sync_playwright() as playwright:
        scrapper = Scrapper(url, playwright)
        ingredients = scrapper._Scrapper__get_sephora_ingredients
        scrapper._Scrapper__close_browser
        ingredients = [ele.lower() for ele in ingredients]
        ingredients_str = " ".join(ingredients)
        harsh_chemicals = ["niacinamide", "niacin"]
        harsh_chemicals_found = []
        harsh_chemical = False
        for chemical in harsh_chemicals:
            if chemical in ingredients_str:
                harsh_chemicals_found.append(chemical)
                harsh_chemical = True
        harsh_chemical_len = len(harsh_chemicals_found)
    return {"harsh_chemical_found": harsh_chemical, "harsh_chemicals_present": harsh_chemicals_found, "number_of_harsh_chemicals": harsh_chemical_len}
