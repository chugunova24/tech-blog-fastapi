from fastapi import APIRouter

from app.core.deps import SessionDep
from app.models.Category import CategoriesPublic, CategoryPublic
from app.services.category import CategoryServices

router = APIRouter()


@router.post("/", response_model=CategoryPublic, status_code=201)
def create_category(session: SessionDep, name: str):
    new_category = CategoryServices.create_category(session=session, name=name)
    return new_category


@router.get("/", response_model=CategoriesPublic)
def get_categories(
    session: SessionDep,
) -> list[dict]:
    categories = CategoryServices.get_all_categories(session)

    return CategoriesPublic(categories=categories, count=len(categories))
