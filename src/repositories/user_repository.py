from .base import BaseRepository
from src.models import User

class UserRepository(BaseRepository[User]):
	def get_by_username(self, username: str) -> User:
		return self.db.query(self.model).filter(self.model.username == username).first()