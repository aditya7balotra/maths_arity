from fastapi import APIRouter, Query, status
from backend.helpers import (
    get_top_reviews,
    insert_review
)
from fastapi.exceptions import HTTPException
from typing import Annotated

reviewRouter = APIRouter()


@reviewRouter.get("/get-top", description= "get the reviews uploaded. Format is {id: [name, institute, comment, rate]}", tags= ["review"])
def get_reviews(top: int | None = 20):
    try:
        return get_top_reviews(top=top)
    except:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= "something unexpected happened")
        

@reviewRouter.post('/insert', description= "upload review", tags= ["review"])
def insert_rvw(institute: Annotated[str, Query(min_length=2, max_length= 50)],
               comment: Annotated[str, Query(min_length= 5, max_length= 1000)],
               rate: Annotated[int, Query(ge = 1, le= 5)], 
               name: Annotated[str, Query(min_length= 2, max_length= 50)]):
    try:
        return [insert_review(name= name, institute= institute, comment= comment, rate = rate)]
    except:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= "something unexpected happened")





