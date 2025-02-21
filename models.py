import sqlalchemy as sq
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func
import uuid

import config

engine = create_async_engine(config.PG_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase, AsyncAttrs):

    @property
    def id_dict(self):
        return {'id': self.id}



# class Token(Base):
#     __tablename__ = 'token'
#
#     id: int = sq.Column(sq.Integer, primary_key=True)
#     token: uuid.UUID = sq.Column(sq.UUID, unique=True, server_default=func.gen_random_uuid())
#     created_time = sq.Column(sq.DateTime, server_default=func.now())
#
#     user_id: int = sq.Column(sq.ForeignKey('user.id'))
#     user = relationship("User", lazy='joined', back_populates='tokens')
#
#     @property
#     def id_dict(self):
#         return {'token': self.token}
#
#
# class User(Base):
#     __tablename__ = 'user'
#
#     id: int = sq.Column(sq.Integer, primary_key=True)
#     name: str = sq.Column(sq.String)
#     password: str = sq.Column(sq.String)
#
#     tokens = relationship(Token, lazy='joined', back_populates='user')
#
#     @property
#     def id_dict(self):
#         return {'id': self.id, 'name': self.name}

class Advertisement(Base):
    __tablename__ = 'advertisement'

    id: int = sq.Column(sq.Integer, primary_key=True)
    title: str = sq.Column(sq.String(length=50), index=True)
    description: str = sq.Column(sq.String(length=255), index=True)
    prise: int = sq.Column(sq.Float, index=True)
    autor: str = sq.Column(sq.String(length=50), index=True)
    created_at = sq.Column(sq.DateTime, server_default=func.now())

    @property
    def dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'prise': self.prise,
            'autor': self.autor,
            'created_at': self.created_at
        }


ORM_OBJ = Advertisement
ORM_CLS = type[Advertisement]


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_orm():
    await engine.dispose()