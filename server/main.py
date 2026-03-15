"""
v0.1
python:  min v3.12
run: uvicorn main:app --host  0.0.0.0 --port 80 --reload
"""
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from user.route import router as user_router
from author.route import router as author_router
from book.route import router as book_router
from genre.route import router as genre_router
from page.route import router as page_router



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(page_router)

app.include_router(user_router, prefix="/api")
app.include_router(author_router, prefix="/api")
app.include_router(genre_router, prefix="/api")
app.include_router(book_router, prefix="/api")

origins = [
    "http://localhost",
    ]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.route('/')
def main_page(request: Request):
    return RedirectResponse(url="/page")
