from fastapi import FastAPI
from fastapi import Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sys
sys.path.append("harmoniz")  # Append directory, not the file
from fileSecurity import fileSecurity
from toolCall import parse

app = FastAPI()

app.mount("/frontpage", StaticFiles(directory="frontpage"), name="frontpage") #because sys fucking sucks

#uvicorn main:app --reload

@app.get("/")
def homepage():
    return FileResponse('frontpage/website.html')

class Item(BaseModel):
    name: str
    data: str

@app.post("/items/")
def create_item(item: Item):
    file_name = "unpreparedMusic.musicxml"
    open(file_name, 'w').close()
    f = open(file_name, "a")
    f.write(item.data)
    f.close()
    if not fileSecurity(file_name):
        return "Music cannot have any written chords"
    parse(file_name, "placeHolder")

    #with open("results.musicxml", 'r') as file:
        #return file.read().replace("\n  ", "")
    with open("results.musicxml", "r") as file:
        content = file.read()
    return Response(
        content=content,
        media_type="application/vnd.recordare.musicxml+xml"
    )
#prevent spamming on the front end side