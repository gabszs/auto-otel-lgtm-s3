from fastapi import APIRouter
from fastapi import Request

router = APIRouter(tags=["Password-Generator"])


@router.get("/health")
async def health():
    return {"status": "alive"}


@router.get("/debug")
async def debug(request: Request):
    return {"root_path": request.scope.get("root_path")}
