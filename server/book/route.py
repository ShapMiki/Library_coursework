from fastapi import APIRouter, Request, Response, status, Depends
from fastapi.responses import StreamingResponse
from typing import Optional, Union

from book.schemas import *
from book.dao import BookDAO
from book.service import generate_report
from genre.model import Genre
from genre.dao import  GenreDAO
from author.model import Author
from user.model import User


router = APIRouter(
    prefix="/book",
    tags=["/book"],
)


@router.get("/status")
async def root():
    return {"status": 200, "details": "user api work"}

@router.post("/edit")
async def edit_books(data: SBookDataSet):
    book_data = data.book_data
    print(book_data)

    if not book_data:
        books = await BookDAO.find_all()
        return {"book_data": books}
    for book in book_data:
        genre_input = book.get('genre_id')
        try:
            book['genre_id'] = int(genre_input)
        except:
            genre_id = await GenreDAO.get_id_by_name(genre_input)
            if genre_id:
                book['genre_id'] = genre_id

        await BookDAO.update_one(book)


@router.get("/{{book_id}}")
async def get_book(book_id: int):
    if not book_id:
        books = await BookDAO.find_all()
        return books
    else:
        book = await BookDAO.find_by_id(book_id)
        return book

@router.post("/")
async def create_book(book: SBook):
    book = await BookDAO.add_one(book)
    return book

@router.get("/all")
async def get_all_books(
    title: Optional[str] = None,
    genre_id: Optional[Union[int, str]] = None,
    sort_by: str = "title",
    order: str = "asc"
):
    safe_genre_id = int(genre_id) if genre_id and str(genre_id).isdigit() else None

    books = await BookDAO.find_filtered(
        title=title,
        genre_id=safe_genre_id,
        sort_by=sort_by,
        order=order
    )
    return {"books": books}

@router.delete("/{book_id}")
async def delete_book(book_id: int):
    result = await BookDAO.delete_by_id(book_id)
    if result:
        return {"status": "success", "message": f"Книга {book_id} удалена"}
    return {"status": "error", "message": "Книга не найдена"}

@router.get("/ids/{book_id}")
async def get_book_ids(book_id: int):
    data = await BookDAO.get_ids(book_id)
    return data


@router.post("/report")
async def report(data: dict):
    file_stream = await generate_report(data)

    docx_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    return StreamingResponse(
        file_stream,
        media_type=docx_type,
        headers={"Content-Disposition": "attachment; filename=report.docx"}
    )
