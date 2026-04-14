from backend.config import URL
from sqlalchemy import create_engine, insert, select, delete
# from sqlalchemy.orm import sessionmaker, declarative_base
from .models import reviews_table, reviews_metadata

class DbService:
    def __init__(self):

        self.engine = create_engine(
            URL,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=1800,
            connect_args={
                "ssl": {"ssl_mode": "REQUIRED"}
            }
        )
        # reviews_metadata.drop_all(self.engine)
        self.create_table()

    def create_table(self):
        reviews_metadata.create_all(self.engine)

    def insert_review(self, institute, comment, rate, name):
        insert_query = insert(reviews_table).values(name = name, institute = institute, comment = comment, rate = rate)
        try:
            with self.engine.begin() as conn:
                result = conn.execute(insert_query)
        except:
            raise Exception("insert review failed")
        
        return result.inserted_primary_key[0]

    def get_reviews(self, top: int) -> list:
        top_results = []
        top_query = select(
            reviews_table.c.id,
            reviews_table.c.name,
            reviews_table.c.institute,
            reviews_table.c.comment,
            reviews_table.c.rate
        ).order_by(reviews_table.c.id.desc()).limit(top)
        with self.engine.connect() as conn:
            for result in conn.execute(top_query):
                top_results.append(result)

        return top_results

    def reset_review_table(self):
        delete_query = delete(reviews_table)
        try:
            with self.engine.begin() as conn:
                conn.execute(delete_query)
        except:
            raise Exception("reset review table failed")

db = DbService()