from fastapi import FastAPI
from fastapi import Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any
import sys
import json
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
    style: str
    data: str

class ComplexItem(BaseModel):
    name: str
    data: Dict[str, Any]

@app.post("/rules/")
def update_rule(item: ComplexItem):
    print(type(item.data))
    try:
        with open('harmoniz/style_completion.json', 'r+') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}

            # Add or update the item in the JSON data
            data[item.name] = item.data

            # Move the file pointer to the beginning of the file to overwrite the content
            f.seek(0)
            json.dump(data, f, indent=4)

            # Truncate the file to remove any remaining old content
            f.truncate()
            
        return {"status": "updated", "name": item.name}
    except FileNotFoundError:
        return {"status": "error", "message": "JSON file not found"}


@app.post("/items/")
def create_item(item: Item):
    file_name = "unpreparedMusic.musicxml" 
    
    #clear file
    open(file_name, 'w').close()
    f = open(file_name, "a")
    f.write(item.data)
    f.close()
    parse(file_name, item.style)

    with open("results.musicxml", "r") as file:
        content = file.read()
    return Response(
        content=content,
        media_type="application/vnd.recordare.musicxml+xml"
    )
#prevent spamming on the front end side