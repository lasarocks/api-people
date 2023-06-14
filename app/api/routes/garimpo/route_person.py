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
    Document,
    GlobalPerson
)



from app.models.schemas.garimpa import(
    SourceSchemaAdd,
    PersonSchemaAdd,
    PersonSchemaListById,
    AddressSchemaAdd,
    ContactSchemaAdd,
    DocumentTypeSchemaAdd,
    DocumentSchemaAdd,
    PersonSchemaAddPremium,
    AddressSchemaAddAPI,
    ContactSchemaAddAPI,
    DocumentSchemaAddAPI,
    PersonSchemaAddPremiumMass
)



router = APIRouter()



@router.get(
    '/person/random'
)
def give_random(
    response: Response,
    db: Session = Depends(get_db)
):
    temp = Person.random_person(session=db)
    if temp:
        return {
            "error": False,
            "data": {
                "id": temp.id,
                "name": temp.name,
                "birthday": temp.birthday,
                "document": temp.document,
                "source_id": temp.source_id,
                "date_created": temp.date_created,
                "addresses": {
                    "total": len(temp.address_data),
                    "data": temp.address_data
                },
                "contacts": {
                    "total": len(temp.contact_data),
                    "data": temp.contact_data
                },
                "documents": {
                    "total": len(temp.document_data),
                    "data": temp.document_data
                }
            }
        }
    else:
        return {
            "error": True,
            "message": "Couldnt get api key"
        }




@router.get(
    '/person/{document}'
)
def find_person_by_document(
    document: str,
    response: Response,
    db: Session = Depends(get_db)
):
    temp = Person.find_by_person_fields(
        session=db,
        v_find=document
    )
    if temp:
        data_out = []
        for row in temp:
            temp_row_data = {
                "id": row.id,
                "name": row.name,
                "birthday": row.birthday,
                "document": row.document,
                "source_id": row.source_id,
                "date_created": row.date_created,
                "addresses": {
                    "total": len(row.address_data),
                    "data": row.address_data
                },
                "contacts": {
                    "total": len(row.contact_data),
                    "data": row.contact_data
                },
                "documents": {
                    "total": len(row.document_data),
                    "data": row.document_data
                }
            }
            data_out.append(temp_row_data)
        return {
            "error": False,
            "total": len(data_out),
            "data": data_out
        }
    else:
        return {
            "error": True,
            "message": "Couldnt get api key"
        }


@router.get(
    '/person'
)
def list_all_person(
    response: Response,
    db: Session = Depends(get_db)
):
    temp = Person.list_all(
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
    '/person'
)
def create_person(
    item: PersonSchemaAdd,
    response: Response,
    db: Session = Depends(get_db)
):
    temp = Person.create(
        session=db,
        person_data=item
    )
    if temp:
        return {
            "error": False,
            "data": {
                "id": temp.id,
                "name": temp.name,
                "birthday": temp.birthday,
                "document": temp.document,
                "source_id": temp.source_id,
                "date_created": temp.date_created
            }
        }
    else:
        return {
            "error": True,
            "message": "Couldnt get api key"
        }





@router.post(
    '/person_all_mass'
)
def create_person_premium_mass(
    item: PersonSchemaAddPremiumMass,
    response: Response,
    db: Session = Depends(get_db)
):
    for person in item.persons:
        temp_create_person = Person.create(
            session=db,
            person_data=PersonSchemaAdd(**person.dict())
        )
        if temp_create_person:
            for address in person.addresses:
                avaddr = Address.create(
                    session=db,
                    data_item=AddressSchemaAddAPI(person_id=temp_create_person.id, **address.dict())
                )
            for contact in person.contacts:
                avc = Contact.create(
                    session=db,
                    data_item=ContactSchemaAddAPI(person_id=temp_create_person.id, **contact.dict())
                )
            for document in person.documents:
                avd = Document.create(
                    session=db,
                    data_item=DocumentSchemaAddAPI(person_id=temp_create_person.id, **document.dict())
                )
    return {"ok": "ok"}



@router.post(
    '/person_all'
)
def create_person_premium(
    item: PersonSchemaAddPremium,
    response: Response,
    db: Session = Depends(get_db)
):
    temp_create_person = Person.create(
        session=db,
        person_data=PersonSchemaAdd(**item.dict())
    )
    if temp_create_person:
        for address in item.addresses:
            if not temp_create_person.exists_address(zipcode=address.zipcode, number=address.number):
                avaddr = Address.create(
                    session=db,
                    data_item=AddressSchemaAddAPI(person_id=temp_create_person.id, **address.dict())
                )
        for contact in item.contacts:
            if not temp_create_person.exists_contact(type_id=contact.type_id, value=contact.value):
                avc = Contact.create(
                    session=db,
                    data_item=ContactSchemaAddAPI(person_id=temp_create_person.id, **contact.dict())
                )
        for document in item.documents:
            if not temp_create_person.exists_document(type_id=document.type_id, number=document.number):
                avd = Document.create(
                    session=db,
                    data_item=DocumentSchemaAddAPI(person_id=temp_create_person.id, **document.dict())
                )
    return item
    temp = Person.create(
        session=db,
        person_data=item
    )
    if temp:
        return {
            "error": False,
            "data": {
                "id": temp.id,
                "name": temp.name,
                "birthday": temp.birthday,
                "document": temp.document,
                "source_id": temp.source_id,
                "date_created": temp.date_created
            }
        }
    else:
        return {
            "error": True,
            "message": "Couldnt get api key"
        }





@router.post(
    '/personglobal'
)
def create_person_global(
    response: Response,
    db: Session = Depends(get_db)
):
    temp = GlobalPerson.create(
        session=db,
        data={}
    )
    if temp:
        return {
            "error": False,
            "data": {
                "id": temp.id,
                "date_created": temp.date_created
            }
        }
    else:
        return {
            "error": True,
            "message": "Couldnt get api key"
        }




@router.put(
    '/person'
)
def update_person(
    item: PersonSchemaAdd,
    response: Response,
    db: Session = Depends(get_db)
):
    temp = Person.create(
        session=db,
        person_data=item
    )
    if temp:
        return {
            "error": False,
            "data": {
                "id": temp.id,
                "name": temp.name,
                "birthday": temp.birthday,
                "document": temp.document,
                "source_id": temp.source_id,
                "date_created": temp.date_created
            }
        }
    else:
        return {
            "error": True,
            "message": "Couldnt get api key"
        }





@router.delete(
    '/person/{id}'
)
def delete_person_by_id(
    document: str,
    response: Response,
    db: Session = Depends(get_db)
):
    temp = Person.find_by_document(
        session=db,
        document=document
    )
    if temp:
        return {
            "error": False,
            "data": {
                "id": temp.id,
                "name": temp.name,
                "birthday": temp.birthday,
                "document": temp.document,
                "source_id": temp.source_id,
                "date_created": temp.date_created
            }
        }
    else:
        return {
            "error": True,
            "message": "Couldnt get api key"
        }


