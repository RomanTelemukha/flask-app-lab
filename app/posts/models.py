from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .. import db

if TYPE_CHECKING:
    from ..users.models import User

post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(db.String(150), nullable=False)
    content: Mapped[str] = mapped_column(db.Text, nullable=False)
    posted: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow)
    category: Mapped[str | None] = mapped_column(
        db.Enum("news", "publication", "tech", "other", name="post_category")
    )
    is_active: Mapped[bool] = mapped_column(db.Boolean, default=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="posts")
    tags: Mapped[list["Tag"]] = relationship(secondary=post_tags, back_populates="posts")
    def __repr__(self):
        return f"<Post {self.id}: {self.title}>"

class Tag(db.Model):
    __tablename__ = 'tags'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String, unique=True, nullable=False)
    posts: Mapped[list["Post"]] = relationship(secondary=post_tags, back_populates="tags")