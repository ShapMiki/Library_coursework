from fastapi import APIRouter, Request, Response, status, Depends



router = APIRouter(
    prefix="/genre",
    tags=["genre"],
)


@router.get("/")
async def root():
    return {"status": 200, "details": "user api work"}
