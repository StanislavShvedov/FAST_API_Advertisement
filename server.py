from fastapi import FastAPI
from sqlalchemy import select

from schema import (
    CreateAdvertRequest, CreateAdvertResponse,
    UpdateAdvertRequest, UpdateAdvertResponse,
    GetAdvertResponse, SearchAdvertResponse,
    DeleteAdvertResponse
)

from lifespan import lifespan
import crud
from dependency import SessionDependency
from models import Advertisement
from constants import SUCCESS_RESPONSE

app = FastAPI(
    title='AdvertisementAPI',
    terms_of_service='',
    description='Advertisement Service',
    lifespan=lifespan
)


@app.post('/api/v1/advertisement', tags=['advertisement'], response_model=CreateAdvertResponse)
async def create_advertisement(advertisement: CreateAdvertRequest, session: SessionDependency):
    advert_dict = advertisement.dict(exclude_unset=True)
    advert_orm_obj = Advertisement(**advert_dict)
    await crud.add_item(session, advert_orm_obj)

    return advert_orm_obj.id_dict


@app.get('/api/v1/advertisement/{advertisement_id}', tags=['advertisement'], response_model=GetAdvertResponse)
async def get_advertisement(advertisement_id: int, session: SessionDependency):
    advert_orm_obj = await crud.get_item_by_id(session=session, orm_cls=Advertisement, item_id=advertisement_id)
    return advert_orm_obj.dict


@app.get('/api/v1/advertisement/', tags=['advertisement'], response_model=SearchAdvertResponse)
async def search_advertisement(session: SessionDependency,
                               title: str,
                               description: str = False,
                               prise: str = False,
                               autor: str = False
                               ):
    query = select(Advertisement).where(Advertisement.title == title,
                                        Advertisement.description == description,
                                        Advertisement.prise == float(prise),
                                        Advertisement.autor == autor).limit(1000)
    advertisements = await session.scalars(query)

    return {'results': [advertisement.dict for advertisement in advertisements]}


@app.patch('/api/v1/advertisement/{advertisement_id}', tags=['advertisement'], response_model=UpdateAdvertResponse)
async def update_advertisement(advertisement_id: int,
                               advertisement_data: UpdateAdvertRequest,
                               session: SessionDependency):
    advert_orm_obj = await crud.get_item_by_id(session=session, orm_cls=Advertisement, item_id=advertisement_id)
    for field, values in advert_orm_obj.dict.items():
        setattr(advert_orm_obj, field, values)
    await crud.add_item(session, advert_orm_obj)

    return SUCCESS_RESPONSE


@app.delete('/api/v1/advertisement/{advertisement_id}', tags=['advertisement'], response_model=DeleteAdvertResponse)
async def delete_advertisement(advertisement_id: int, session: SessionDependency):
    advert_orm_obj = await crud.get_item_by_id(session=session, orm_cls=Advertisement, item_id=advertisement_id)
    await crud.delete_item(session, advert_orm_obj)

    return SUCCESS_RESPONSE
