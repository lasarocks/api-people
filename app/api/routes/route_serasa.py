import os
from typing import List
from sqlalchemy.orm import Session
from fastapi import(
    Depends,
    Response,
    status,
    APIRouter,
    File,
    UploadFile
)
from fastapi.responses import JSONResponse


from app.core.database import get_db

from app.exceptions.serasadb_exceptions import(
    NoNameGivenError
)


from app.models.domain.serasadb import(
    serasaData
)



from app.models.domain.garimpa import(
    Source,
    Person,
    Address,
    Contact
)


from app.models.schemas.serasa import(
    PersonDocumentSearch,
    PersonNameSearch,
    PersonFindResponse,
    PersonNamePlusSearch
)


from app.models.schemas.garimpa import(
    SourceSchemaAdd,
    PersonSchemaAdd,
    AddressSchemaAdd,
    ContactSchemaAdd
)



router = APIRouter()





@router.get(
    '/cpf/{cpf_find}',
    status_code=status.HTTP_200_OK
)
def cpf(
    cpf_find: str,
    response: Response,
    db: Session = Depends(get_db)
):
    temp_response = serasaData.find_by_cpf(session=db, cpf=cpf_find)
    if temp_response:
        return temp_response
    else:
        return {
            "error": True,
            "message": "Couldnt get api key"
        }






@router.post(
    '/name',
    status_code=status.HTTP_200_OK
)
def namelike(
    item: PersonNameSearch,
    response: Response,
    db: Session = Depends(get_db)
):
    if not item.name:
        return {
            "error": True,
            "message": "No Name Given"
        }
    temp_response = serasaData.find_by_name_like(session=db, name_like=item.name)
    if temp_response:
        data = []
        for row in temp_response:
            temp_data = {
                'name': row.name,
                'document': row.cpf,
                'birthday': row.birth,
                'gender': row.genre
            }
            data.append(temp_data)
        return {
            "error": False,
            "data": data
        }
    else:
        return {
            "error": True,
            "message": "Couldnt get api key"
        }




@router.post(
    '/name-plus',
    status_code=status.HTTP_200_OK
)
def namelikeplus(
    item: PersonNamePlusSearch,
    response: Response,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    if not item.first_name and not item.middle_name and not item.last_name:
        return {
            "error": True,
            "message": "No Name Given"
        }
    temp_response = serasaData.find_by_partial_name(
        session=db,
        first_name=item.first_name,
        middle_name=item.middle_name,
        last_name=item.last_name,
        birth_day=item.birth_day,
        birth_month=item.birth_month,
        birth_year=item.birth_year,
        limit=limit
    )
    if temp_response:
        data = []
        if len(temp_response)>50:
            return {
                "error": True,
                "message": "Too Much Information",
                "detail": len(temp_response)
            }
        for row in temp_response:
            temp_data = {
                'name': row.name,
                'document': row.cpf,
                'birthday': row.birth,
                'gender': row.genre
            }
            data.append(temp_data)
        return {
            "error": False,
            "data": data
        }
    elif temp_response != False:
        return {
            "error": True,
            "message": "No Results"
        }
    else:
        return {
            "error": True,
            "message": "FAILED"
        }










