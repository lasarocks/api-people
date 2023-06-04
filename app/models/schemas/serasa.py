from datetime import date
from pydantic import Field
from datetime import datetime
from app.models.schemas.base import baseSchema
from typing import (
    Union,
    Optional
)




class PersonDocumentSearch(baseSchema):
    cpf: str



class PersonNameSearch(baseSchema):
    name: str



class PersonNamePlusSearch(baseSchema):
    first_name: Optional[str] =  ''
    middle_name: Optional[str] =  ''
    last_name: Optional[str] =  ''
    birth_day: Optional[int] =  0
    birth_month: Optional[int] =  0
    birth_year: Optional[int] =  0



class PersonFindResponse(baseSchema):
    cpf: str
    name: str
    birth: str
    genre: str


