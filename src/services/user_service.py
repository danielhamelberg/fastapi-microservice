from src.repositories.user_repository import UserRepository
from src.schemas import UserCreate, User
from src.models import User as UserModel
from auth.utils import get_password_hash
from sqlalchemy.orm import Session


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(UserModel)
        self.db = db

    def create_user(self, user: UserCreate) -> User:
        hashed_password = get_password_hash(user.password)
        db_user = self.repository.create(self.db, obj_in=UserCreate(email=user.email, hashed_password=hashed_password))
        return User.from_orm(db_user)

    def get_user(self, user_id: int) -> User:
        user = self.repository.get(self.db, id=user_id)
        return User.from_orm(user) if user else None

    def get_user_by_email(self, email: str) -> User:
        user = self.repository.get_by_email(self.db, email=email)
        return User.from_orm(user) if user else None
