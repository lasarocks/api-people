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
    DocumentSchemaAdd,
    DocumentSchemaAddAPI
)



router = APIRouter()


#DOCUMENT TYPE

@router.get(
    '/{person_id}/document'
)
def list_all_documents(
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


@router.get(
    '/{person_id}/document/{id}'
)
def get_document_by_id(
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
    '/document'
)
def create_document_api(
    item: DocumentSchemaAddAPI,
    response: Response,
    db: Session = Depends(get_db)
):
    temp = Document.create(
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
    '/{person_id}/document'
)
def create_document(
    person_id: str,
    item: DocumentSchemaAdd,
    response: Response,
    db: Session = Depends(get_db)
):
    item_api = DocumentSchemaAddAPI(person_id=person_id, **item.dict())
    temp = Document.create(
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




# @router.post(
#     '/document-type'
# )
# def create_document_type(
#     item: DocumentTypeSchemaAdd,
#     response: Response,
#     db: Session = Depends(get_db)
# ):
#     temp = DocumentType.create(
#         session=db,
#         data=item
#     )
#     if temp:
#         return {
#             "error": False,
#             "data": temp
#         }
#     else:
#         return {
#             "error": True,
#             "message": "Couldnt get api key"
#         }









# @router.put(
#     '/document-type'
# )
# def update_document_type(
#     item: SourceSchemaAdd,
#     response: Response,
#     db: Session = Depends(get_db)
# ):
#     temp = Source.create(
#         session=db,
#         source_data=item
#     )
#     if temp:
#         return {
#             "error": False,
#             "data": {
#                 "id": temp.id,
#                 "description": temp.description,
#                 "author": temp.author,
#                 "date": temp.date,
#                 "date_created": temp.date_created
#             }
#         }
#     else:
#         return {
#             "error": True,
#             "message": "Couldnt get api key"
#         }



@router.delete(
    '/{person_id}/document/{id}'
)
def delete_documentby_id(
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