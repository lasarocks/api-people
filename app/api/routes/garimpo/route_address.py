import os
from typing import List
from sqlalchemy.orm import Session
from fastapi import(
    Depends,
    Response,
    status,
    APIRouter,
    HTTPException
)
from fastapi.responses import JSONResponse


from app.core.database import get_db

import json


from app.models.domain.garimpa import(
    Source,
    Person,
    Address,
    Contact,
    DocumentType,
    Document
)



from app.models.schemas.garimpa import(
    SourceSchemaAdd,
    PersonSchemaAdd,
    PersonSchemaListById,
    AddressSchema,
    AddressSchemaAdd,
    AddressSchemaAddAPI,
    ContactSchemaAdd,
    DocumentTypeSchemaAdd,
    DocumentSchemaAdd
)

from app.exceptions.person_exceptions import(
    PersonNotFound
)


from app.exceptions.garimpa_exceptions import(
    ItemNotFound
)

from pydantic import parse_obj_as


router = APIRouter()





@router.get(
    '/{person_id}/address'
)
def list_all_address(
    person_id: str,
    response: Response,
    db: Session = Depends(get_db)
):
    addresses = Address.list_by_person_id(
        session=db,
        person_data_id=person_id
    )
    if addresses:
        return {"data": addresses}
    else:
        raise ItemNotFound(message=f'didnt find any data to value --> {person_id}')
        return JSONResponse(
            content={"error": True, "message": "Couldn't get address data"},
            status_code=404,
        )



@router.get(
    '/{person_id}/address/{id}'
)
def list_address_by_id(
    response: Response,
    db: Session = Depends(get_db)
):
    temp = Address.list_all(
        session=db
    )
    if temp:
        temp_data = []
        for row in temp:
            temp_data.append(row)
        return {
            "error": False,
            "data": temp_data
        }
    else:
        return {
            "error": True,
            "message": "Couldnt get api key"
        }



# @router.get(
#     '/{person_id}/address'
# )
# def list_address_by_person_id(
#     response: Response,
#     db: Session = Depends(get_db)
# ):
#     temp = Address.list_all(
#         session=db
#     )
#     if temp:
#         temp_data = []
#         for row in temp:
#             temp_data.append(row)
#         return {
#             "error": False,
#             "data": temp_data
#         }
#     else:
#         return {
#             "error": True,
#             "message": "Couldnt get api key"
#         }





@router.post(
    '/address'
)
def create_address_api(
    item: AddressSchemaAddAPI,
    response: Response,
    db: Session = Depends(get_db)
):
    temp = Address.create(
        session=db,
        data_item=item
    )
    if temp:
        return {
            "error": False,
            "data": temp
        }
    else:
        return {
            "error": True,
            "message": "Couldnt get api key"
        }





@router.post(
    '/{person_id}/address'
)
def create_address(
    person_id: str,
    item: AddressSchemaAdd,
    response: Response,
    db: Session = Depends(get_db)
):
    item_api = AddressSchemaAddAPI(person_id=person_id, **item.dict())
    temp = Address.create(
        session=db,
        data_item=item_api
    )
    if temp:
        return {
            "error": False,
            "data": temp
        }
    else:
        return {
            "error": True,
            "message": "Couldnt get api key"
        }




@router.delete(
    '/{person_id}/address/{id}'
)
def delete_address_by_id(
    response: Response,
    db: Session = Depends(get_db)
):
    temp = Address.list_all(
        session=db
    )
    if temp:
        temp_data = []
        for row in temp:
            temp_data.append(row)
        return {
            "error": False,
            "data": temp_data
        }
    else:
        return {
            "error": True,
            "message": "Couldnt get api key"
        }