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


#DOCUMENT TYPE

@router.get(
    '/document-type'
)
def list_all_document_type(
    response: Response,
    db: Session = Depends(get_db)
):
    temp = DocumentType.list_all(
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
    '/document-type/{id}'
)
def get_by_id_document_type(
    id: str,
    response: Response,
    db: Session = Depends(get_db)
):
    temp = Source.list_all(
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
    '/document-type'
)
def create_document_type(
    item: DocumentTypeSchemaAdd,
    response: Response,
    db: Session = Depends(get_db)
):
    temp = DocumentType.create(
        session=db,
        data=item
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









@router.put(
    '/document-type'
)
def update_document_type(
    item: SourceSchemaAdd,
    response: Response,
    db: Session = Depends(get_db)
):
    temp = Source.create(
        session=db,
        source_data=item
    )
    if temp:
        return {
            "error": False,
            "data": {
                "id": temp.id,
                "description": temp.description,
                "author": temp.author,
                "date": temp.date,
                "date_created": temp.date_created
            }
        }
    else:
        return {
            "error": True,
            "message": "Couldnt get api key"
        }



@router.delete(
    '/document-type/{id}'
)
def delete_document_type(
    id: str,
    response: Response,
    db: Session = Depends(get_db)
):
    temp = Source.create(
        session=db,
        source_data=id
    )
    if temp:
        return {
            "error": False,
            "data": {
                "id": temp.id,
                "description": temp.description,
                "author": temp.author,
                "date": temp.date,
                "date_created": temp.date_created
            }
        }
    else:
        return {
            "error": True,
            "message": "Couldnt get api key"
        }