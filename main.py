from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import sys

sys.path.append("harmoniz")  # Append directory, not the file

from toolCall import parse

app = FastAPI()

app.mount("/frontpage", StaticFiles(directory="frontpage"), name="frontpage")

#uvicorn main:app --reload

@app.get("/")
def homepage():
    return FileResponse('frontpage/website.html')

class Item(BaseModel):
    name: str
    data: str

@app.post("/items/")
def create_item(item: Item):
    print(item)
    return "thanks nigga"