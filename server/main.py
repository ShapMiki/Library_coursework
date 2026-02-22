"""
v0.1
python:  min v3.12
run: uvicorn main:app --host  0.0.0.0 --port 80 --reload
"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from user.route import router as user_router
from author.route import router as author_router
from book.route import router as book_router
from genre.route import router as genre_router



app = FastAPI()


app.include_router(user_router)
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

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")
