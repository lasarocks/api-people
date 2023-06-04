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


from enum import Enum

router = APIRouter()



class Keys(str, Enum):
    document = "document"
    register_gov = "register_gov"



@router.get(
    '/load-by-document/{document}'
)
def load_by_document(
    document: str,
    response: Response,
    db: Session = Depends(get_db)
):
    return {"hi": True}




@router.get(
    '/load-by-{key}/{value}'
)
def load_by_custom(
    key: Keys,
    value: int,
    response: Response,
    db: Session = Depends(get_db)
):
    return {
        "value": key
    }




