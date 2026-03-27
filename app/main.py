from typing import Annotated, List
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from providers import Multisender


multisender = Multisender()


app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory="static"), name="static")


@app.get('/', response_class=HTMLResponse)
def index_page(request: Request):
    return templates.TemplateResponse(
        name='index.html',
        request=request
    )


@app.post('/send')
async def send(
    text: str = Form(...),
    providers: Annotated[List[str], Form(...)] = []
):
    return await multisender.send_all(text)
    


if __name__ == '__main__':
    uvicorn.run(app)