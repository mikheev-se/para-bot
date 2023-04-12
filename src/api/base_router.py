from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from src.api.query_router import query_router
from src.api.names_router import names_router
from src.api.surnames_router import surnames_router
from src.api.subjects_router import subjects_router

router = APIRouter()

router.include_router(query_router)
router.include_router(names_router)
router.include_router(surnames_router)
router.include_router(subjects_router)


@router.get('/', include_in_schema=False)
def root():
    return RedirectResponse('/docs')
