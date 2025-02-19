import sqlalchemy as sq
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func

import config

engine = create_async_engine(config.PG_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase, AsyncAttrs):

    @property
    def id_dict(self):
        return {'id': self.id}


class Advertisement(Base):
    __tablename__ = 'advertisement'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=50), index=True)
    description = sq.Column(sq.String(length=255), index=True)
    prise = sq.Column(sq.Float, index=True)
    autor = sq.Column(sq.String(length=50), index=True)
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