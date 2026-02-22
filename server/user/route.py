from fastapi import APIRouter, Request, Response, status, Depends



router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get("/")
async def root():
    return {"status": 200, "details": "user api work"}
