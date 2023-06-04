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
    ContactType,
    DocumentType,
    Document
)



from app.models.schemas.garimpa import(
    SourceSchemaAdd,
    PersonSchemaAdd,
    AddressSchemaAdd,
    ContactSchemaAdd,
    ContactTypeSchemaAdd,
    ContactSchemaAddAPI,
    DocumentTypeSchemaAdd,
    DocumentSchemaAdd
)



router = APIRouter()




@router.get(
    '/{person_id}/contact'
)
def list_all_contact(
    person_id: str,
    response: Response,
    db: Session = Depends(get_db)
):
    print('eh po...')
    contacts = Contact.list_by_person_id(
        session=db,
        person_data_id=person_id
    )
    if contacts:
        return {"data": contacts}
        contact_data = [contact.to_dict() for contact in contacts]
        return JSONResponse(
            content={"error": False, "data": contact_data},
            status_code=200
        )
    else:
        return JSONResponse(
            content={"error": True, "message": "Couldn't get address data"},
            status_code=404,
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
    '/{person_id}/contact/{id}'
)
def list_contact_by_id(
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
    '/contact/type'
)
def add_contact_type(
    item: ContactTypeSchemaAdd,
    response: Response,
    db: Session = Depends(get_db)
):
    temp = ContactType.create(
        session=db,
        contact_type_data=item
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
    '/contact'
)
def add_contact_api(
    item: ContactSchemaAddAPI,
    response: Response,
    db: Session = Depends(get_db)
):
    temp = Contact.create(
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
    '/{person_id}/contact'
)
def add_contact(
    person_id: str,
    item: ContactSchemaAdd,
    response: Response,
    db: Session = Depends(get_db)
):
    item_api = ContactSchemaAddAPI(person_id=person_id, **item.dict())
    temp = Contact.create(
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
    '/{person_id}/contact/{id}'
)
def delete_contact_by_id(
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