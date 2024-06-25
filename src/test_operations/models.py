from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from database import Base



class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True)
    user_mail = Column(String(100), unique=True)
    hashed_password = Column(String(length=1024), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    content = Column(String(100))
    user_id = Column(Integer, ForeignKey(User.id))

    author = relationship("User", back_populates="posts")








    # from sqlalchemy import Table, Column, Integer, String, ForeignKey
    # from sqlalchemy.orm import relationship
    # from .database import metadata, engine
    #
    # # User model
    # users = Table(
    #     "users",
    #     metadata,
    #     Column("id", Integer, primary_key=True, index=True),
    #     Column("name", String, index=True),
    #     Column("email", String, unique=True, index=True)
    # )
    #
    # # Book model
    # books = Table(
    #     "books",
    #     metadata,
    #     Column("id", Integer, primary_key=True, index=True),
    #     Column("title", String, index=True),
    #     Column("author", String, index=True)
    # )
    #
    # # Order model
    # orders = Table(
    #     "orders",
    #     metadata,
    #     Column("id", Integer, primary_key=True, index=True),
    #     Column("user_id", Integer, ForeignKey("users.id")),
    #     Column("book_id", Integer, ForeignKey("books.id")),
    # )
    #
    # metadata.create_all(bind=engine)