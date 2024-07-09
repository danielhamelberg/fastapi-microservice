from .base import BaseRepository
from src.models import Post
from sqlalchemy.orm import Session
from typing import List

class PostRepository(BaseRepository[Post]):
    def get_by_author(self, author_id: int) -> List[Post]:
        return self.db.query(self.model).filter(self.model.author_id == author_id).all()

    def get_recent(self, limit: int = 10) -> List[Post]:
        return self.db.query(self.model).order_by(self.model.created_at.desc()).limit(limit).all()
