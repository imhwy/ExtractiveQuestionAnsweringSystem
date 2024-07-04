"""
Run the code in this file
"""

import uvicorn
from fastapi import FastAPI, status, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.api.routers import inference_router


app = FastAPI()
templates = Jinja2Templates(directory="static/templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def read_root(request: Request):
    """
    Handles GET requests to the root endpoint "/root/".

    Args:
        request (Request): The HTTP request object.

    Returns:
        TemplateResponse: Renders the "index.html" template 
        with the request object passed to the template context.
    """
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) from e

# app.include_router(root_router)
app.include_router(inference_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Run the server
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000
    )
