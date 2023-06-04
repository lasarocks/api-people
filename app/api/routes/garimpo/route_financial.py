import os
from typing import List
from sqlalchemy.orm import Session
from fastapi import(
    Depends,
    Response,
    status,
    APIRouter
)
from fastapi.responses import JSONResponse


from app.core.database import get_db




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
    AddressSchemaAdd,
    ContactSchemaAdd,
    DocumentTypeSchemaAdd,
    DocumentSchemaAdd
)



router = APIRouter()



@router.get(
    '/{person_id}/financial/status'
)
def get_financial_status(
    person_id: str,
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




@router.post(
    '/{person_id}/financial/status'
)
def create_financial_status(
    person_id: str,
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




@router.patch(
    '/{person_id}/financial/status'
)
def update_score_financial_status(
    person_id: str,
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




@router.get(
    '/{person_id}/financial'
)
def list_all_financial_history(
    person_id: str,
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



@router.get(
    '/{person_id}/financial/open-debits'
)
def list_all_financial_open_debits(
    person_id: str,
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



@router.get(
    '/{person_id}/financial/closed-debits'
)
def list_all_financial_closed_debits(
    person_id: str,
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




@router.get(
    '/{person_id}/financial/{id}'
)
def get_debit_financial_by_id(
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
    '/{person_id}/financial'
)
def create_financial_debit(
    person_id: str,
    item: AddressSchemaAdd,
    response: Response,
    db: Session = Depends(get_db)
):
    temp = Address.create(
        session=db,
        address_data=item
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
    '/{person_id}/financial/{id}'
)
def delete_financial_debit_by_id(
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