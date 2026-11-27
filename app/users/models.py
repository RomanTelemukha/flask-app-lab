from typing import TYPE_CHECKING
from flask_login import UserMixin
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db, login_manager, bcrypt

if TYPE_CHECKING:
    from ..posts.models import Post

@login_manager.user_loader
def user_loader(user_id):
    return db.session.get(User, int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    posts: Mapped[list["Post"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User {self.username}>"

    def hash_password(self, password=None):
        raw = password if password is not None else self.password
        self.password = bcrypt.generate_password_hash(raw).decode("utf-8")

    def check_password(self, password):
        try:
            return bcrypt.check_password_hash(self.password, password)
        except ValueError:
            return self.password == password
