from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from user.dependencies import get_current_user

from book.dao import BookDAO
from author.dao import AuthorDAO
from genre.dao import GenreDAO


templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/page",
    tags=["page"],
)


@router.get("/")
async def root(request: Request, user=Depends(get_current_user)):
    if user:
        return RedirectResponse(url="/page/books")
    data = None
    return templates.TemplateResponse("index.html", {"request": request, "data": data})

@router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/registration")
async def login(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})

@router.get("/books")
async def books_page(request: Request, user=Depends(get_current_user)):
    books = await BookDAO.find_all_full()
    data = {
        "books": books
    }

    return templates.TemplateResponse(
        "books.html",
        {
            "request": request,
            "data": data
        }
    )

@router.get("/authors")
async def authors_page(request: Request, user=Depends(get_current_user)):
    authors = await AuthorDAO.find_all()
    data={"authors": authors}
    return templates.TemplateResponse(
        "authors.html",
        {
            "request": request,
            "data": data
        }
    )

@router.get("/genres")
async def genres_page(request: Request, user=Depends(get_current_user)):
    genres = await GenreDAO.find_all()
    data={"genres": genres}
    return templates.TemplateResponse(
        "genres.html",
        {
            "request": request,
            "data": data
        }
    )

@router.get("/book/form")
async def book_form(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("book_form.html", {"request": request})

@router.get("/book/form/{book_id}")
async def book_form(book_id: int, request: Request, user=Depends(get_current_user)):
    if book_id:
        book = await BookDAO.find_by_id(book_id)
        return templates.TemplateResponse("book_edit_form.html", {"request": request, "data": {"book": book}})

@router.get("/books/edit")
async def books_edit_page(request: Request, user=Depends(get_current_user)):

    books = await BookDAO.find_all()

    return templates.TemplateResponse(
        "books_mass_edit.html",
        {
            "request": request,
            "data": {
                "books": books
            }
        }
    )

@router.get("/author/form")
async def book_form(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("author_form.html", {"request": request})

@router.get("/genre/form")
async def book_form(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("genre_form.html", {"request": request})

@router.get("/main-menu")
async def menu(request: Request):
    return templates.TemplateResponse("main_menu.html", {"request": request})

@router.get("/report")
async def menu(request: Request):
    return templates.TemplateResponse("report_form.html", {"request": request})
