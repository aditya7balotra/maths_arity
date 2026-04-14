from backend.db import db
from backend.logs import log


def get_top_reviews(top: int):
    log.info("Getting top reviews")
    top_reviews = db.get_reviews(top= top)
    log.info(f"Top reviews: {top_reviews}")
    data = {}
    # format {"id": [name, institute, comment, rate]}
    for review in top_reviews:
        data[review[0]] = [review[1], review[2], review[3], review[4]]
    return data



def insert_review(name: str, institute: str, comment: str, rate: int) -> int:
    log.info(f"Inserting review: name: {name}, institute: {institute}, comment: {comment}")
    id = db.insert_review(name= name, institute= institute, comment= comment, rate= rate)
    log.info(f"Inserted review id is {id}")
    return id
