from datetime import date
from pydantic import Field, validator
from datetime import datetime
from app.models.schemas.base import baseSchema
from typing import (
    Union,
    Optional,
    List
)






class SourceSchemaAdd(baseSchema):
    description: str
    author: Optional[str] = None
    date: Optional[str] = None






class DocumentTypeSchemaAdd(baseSchema):
    description: str
    key: str





class ContactTypeSchemaAdd(baseSchema):
    description: str
    key: str




class CustomDataTypeSchemaAdd(baseSchema):
    description: str
    base: dict
    key: str








# class DocumentTypeSchemaAdd(baseSchema):
#     description: str



class PersonSchemaListById(baseSchema):
    id: str



class AddressSchema(baseSchema):
    id: str
    description: Optional[str] = None
    name: Optional[str] = None
    prefix: Optional[str] = None
    street: Optional[str] = None
    neighborhood: Optional[str] = None
    zipcode: str
    number: Optional[str] = None
    complement: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    source_id: str
    person_id: str
    date_created: datetime




class AddressSchemaAddBase(baseSchema):
    description: Optional[str] = None
    name: Optional[str] = None
    prefix: Optional[str] = None
    street: Optional[str] = None
    neighborhood: Optional[str] = None
    zipcode: str
    number: Optional[str] = None
    complement: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None



class AddressSchemaAdd(AddressSchemaAddBase):
    source_id: Optional[str] = None
    


class AddressSchemaAddAPI(AddressSchemaAdd):
    person_id: str




class ContactSchemaAddBase(baseSchema):
    description: Optional[str] = None
    type_id: str
    name: Optional[str] = None
    value: str


class ContactSchemaAdd(ContactSchemaAddBase):
    source_id: Optional[str] = None
    


class ContactSchemaAddAPI(ContactSchemaAdd):
    person_id: str




class DocumentSchemaAddBase(baseSchema):
    type_id: str
    description: Optional[str] = None
    date_issuing: Optional[str] = None
    date_expiration: Optional[str] = None
    state_issuing: Optional[str] = None
    issuing_authority: Optional[str] = None
    number: str


class DocumentSchemaAdd(DocumentSchemaAddBase):
    source_id: Optional[str] = None
    

class DocumentSchemaAddAPI(DocumentSchemaAdd):
    person_id: str




class CDCCPanSchema(baseSchema):
    name: Optional[str] = None
    ccpan: str
    name_holder: Optional[str] = None
    expiration: Optional[str] = None
    cvv: Optional[str] = None


class CDPWHashSchema(baseSchema):
    name: Optional[str] = None
    hash: str




class CDBPIXSchema(baseSchema):
    name: Optional[str] = None
    chave: str
    banco: str





class CustomDataSchemaAddBase(baseSchema):
    type_id: str
    description: Optional[str] = None
    value: dict



class CustomDataSchemaAdd(CustomDataSchemaAddBase):
    source_id: Optional[str] = None
    

class CustomDataSchemaAddAPI(CustomDataSchemaAdd):
    person_id: str





class PersonDataSchemaAdd(baseSchema):
    name: str
    birthday: datetime
    source_id: Optional[str] = None
    



class PersonDataSchemaP(PersonDataSchemaAdd):
    person_id: Optional[str] = None




class PersonSchemaAdd(baseSchema):
    name: str
    birthday: str
    #document: str
    source_id: str





class PersonSchemaAddPremium(PersonSchemaAdd):
    addresses: Optional[List[AddressSchemaAddBase]] = None
    contacts: Optional[List[ContactSchemaAddBase]] = None
    documents: Optional[List[DocumentSchemaAddBase]] = None



class PersonSchemaAddPremiumMass(baseSchema):
    persons: List[PersonSchemaAddPremium]



class GlobalPersonAddBase(baseSchema):
    unique_document: str
    person_data: Optional[PersonDataSchemaAdd] = None
    addresses: Optional[List[AddressSchemaAddBase]] = None
    contacts: Optional[List[ContactSchemaAddBase]] = None
    documents: Optional[List[DocumentSchemaAddBase]] = None
    custom: Optional[List[CustomDataSchemaAddBase]] = None



class GlobalPersonAdd(GlobalPersonAddBase):
    source_id: str



class GlobalPersonAddPremiumMass(baseSchema):
    source_id: str
    persons: List[GlobalPersonAddBase]



class GlobalPersonAddSchema(baseSchema):
    source_id: str