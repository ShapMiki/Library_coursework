from fastapi import APIRouter, Request, Response, status, Depends

from book.schemas import *
from book.dao import BookDAO
from genre.model import Genre
from author.model import Author
from user.model import User


router = APIRouter(
    prefix="/book",
    tags=["/book"],
)


@router.get("/")
async def root():
    return {"status": 200, "details": "user api work"}

@router.post("/edit")
async def edit_books(data: SBookDataSet):
    book_data = data.book_data
    if not book_data:
        books = await BookDAO.find_all()
        return {"book_data": books}
    for book in book_data:
        await BookDAO.update_one(book)


@router.get("/books")
async def get_book():
    books = await BookDAO.find_all()
    return books

@router.post("/book")
async def create_book(book: SBook):
    book = await BookDAO.add_one(book)
    return book

