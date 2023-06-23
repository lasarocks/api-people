from sqlalchemy import(
    Column,
    Integer,
    String,
    ForeignKey,
    text,
    and_,
    or_,
    event
)
from sqlalchemy.schema import Table

from sqlalchemy.orm import Session
from sqlalchemy.types import(
    Date,
    Boolean,
    Time,
    DateTime,
    JSON
)
from typing import List, Type, Union

from sqlalchemy.orm import relationship

from app.core.database import Base, engine, SessionLocal         
from datetime import datetime

from app.exceptions.serasadb_exceptions import(
    NoNameGivenError
)
from sqlalchemy.sql import func

from app.exceptions.person_exceptions import(
    PersonNotFound
)


from app.exceptions.garimpa_exceptions import(
    ItemNotFound
)



from app.models.schemas.garimpa import(
    SourceSchemaAdd,
    PersonSchemaAdd,
    PersonDataSchemaAdd,
    AddressSchemaAdd,
    AddressSchemaAddAPI,
    ContactSchemaAdd,
    ContactSchemaAddAPI,
    DocumentTypeSchemaAdd,
    DocumentSchemaAddAPI,
    DocumentSchemaAdd,
    PersonSchemaListById,
    ContactTypeSchemaAdd,
    GlobalPersonAdd,
    GlobalPersonAddSchema,
    CustomDataTypeSchemaAdd,
    CustomDataSchemaAddBase,
    CustomDataSchemaAddAPI,
    CDCCPanSchema,
    CDPWHashSchema,
    CDBPIXSchema
)


import uuid



class CRUDPersonBase:
    @classmethod
    def create(cls: Type[Base], session: Session, data: dict) -> Base:
        obj = cls(**data)
        obj.id = str(uuid.uuid4())
        obj.date_created = datetime.utcnow()
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    @classmethod
    def list_all(cls: Type[Base], session: Session) -> List[Base]:
        return session.query(cls).all()
    
    @classmethod
    def _after_create(cls, connection):
        pass

    @classmethod
    def list_by_id_hide(
        cls: Base, 
        session: Session,
        id: str
    ):
        try:
            return session.query(
                cls
            ).filter_by(
                id=id
            ).first()
        except Exception as err:
            print(f'exception list_by_id - {err}')
        return False
    
    
    

class CRUDByPersonBase(CRUDPersonBase):
    @classmethod
    def list_by_person_id2(
        cls: Base, 
        session: Session,
        person_data_id: str
    ):
        try:
            return session.query(
                cls
            ).filter_by(
                person_id=person_data_id
            ).all()
        except Exception as err:
            print(f'exception list_by_id - {err}')
        return False
    @classmethod
    def list_by_person_id(
        cls: Base, 
        session: Session,
        person_data_id: str
    ):
        try:
            print('passando aki')
            return session.query(
                cls
            ).join(
                Person
            ).filter(
                or_(
                    Person.id==person_data_id,
                    Person.document == person_data_id
                )
            ).all()
        except Exception as err:
            print(f'exception list_by_id - {err}')
        return False






class Source(CRUDPersonBase, Base):
    __tablename__ = 'Source'
    id = Column(String(36), primary_key=True)#
    description = Column(String(255), nullable=False)
    author = Column(String(120), nullable=True, default=None)
    date = Column(DateTime, nullable=True, default=None)
    date_created = Column(DateTime, default=datetime.utcnow())
    source_global = relationship('GlobalPerson', backref='Source')
    # source_persondata = relationship('PersonData', backref='Source')
    # source_address = relationship('Address', backref='Source')
    # source_contact = relationship('Contact', backref='Source')
    # source_document = relationship('Document', backref='Source')
    @classmethod
    def create(
        cls: Type[Base],
        session: Session,
        source_data: SourceSchemaAdd
    ):
        temp_date_datetime = None
        data = source_data.dict()
        if source_data.date:
            temp_date_str = source_data.date
            try:
                temp_date_datetime = datetime.strptime(temp_date_str, "%d/%m/%Y")
            except:
                pass
        data["date"] = temp_date_datetime
        return super().create(session, data)
    @classmethod
    def check_source_exists(cls, session, v_find):
        temp = Source.list_by_id_hide(session=session, id=v_find)
        if not temp:
            raise ItemNotFound(message=f'didnt find any source with value --> {v_find}')
        return temp
        






class GlobalPerson(CRUDPersonBase, Base):
    __tablename__ = "GlobalPerson"
    id = Column(String(36), primary_key=True)
    source_id = Column(String(36), ForeignKey("Source.id"), nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)
    person_data = relationship('Person', backref='GlobalPerson')
    address_data = relationship('Address', backref='GlobalPerson')
    contact_data = relationship('Contact', backref='GlobalPerson')
    document_data = relationship('Document', backref='GlobalPerson')
    custom_data = relationship('CustomData', backref='GlobalPerson')

    @classmethod
    def create(
        cls: Base,
        session: Session,
        person_data: GlobalPersonAdd
    ):
        avoid = Source.check_source_exists(session=session, v_find=person_data.source_id)
        data_person = GlobalPerson.find_by_unique_document(session=session, document=person_data.unique_document)
        if not data_person:
            data_person = super().create(session, GlobalPersonAddSchema(**person_data.dict()).dict())
            if data_person:
                doc_create = Document.create(session=session, data_item=DocumentSchemaAddAPI(person_id=data_person.id, type_id='cpf', number=person_data.unique_document))
                return doc_create.GlobalPerson
        else:
            data_person.source_id = person_data.source_id
        return data_person
    

    @classmethod
    def random_person(cls, session):
        try:
            return session.query(
                cls
            ).outerjoin(
                Person,
                Contact,
                Address,
                Document,
                CustomData
            ).order_by(
                func.random()
            ).limit(
                1
            ).first()
        except Exception as err:
            print(f'exception find_by_document - {err}')
        return False
    

    @classmethod
    def check_global_person_exists(cls, session, v_find):
        temp = GlobalPerson.list_by_id_hide(session=session, id=v_find)
        if not temp:
            raise ItemNotFound(message=f'didnt find any person with value --> {v_find}')
        return temp
    
    @classmethod
    def find_by_person_fields(cls, session, v_find):
        try:
            select = session.query(
                cls
            ).outerjoin(
                Person,
                Contact,
                Address,
                Document,
                CustomData
            ).filter(
                or_(
                    Person.id == v_find,
                    #Person.document == v_find,
                    Contact.value == v_find,
                    Document.number == v_find
                )
            )
            response = select.all()
            if response:
                return response    
        except Exception as err:
            print(f'exception find_by_document - {err}')
        raise ItemNotFound(message=f'didnt find any person with value --> {v_find}')
        return False
    @classmethod
    def find_by_unique_document(cls, session, document):
        try:
            select = session.query(
                cls
            ).outerjoin(
                Document
            ).filter(
                and_(
                    Document.number==document,
                    Document.type_id=='cpf'
                )
            )
            return select.first()
        except Exception as err:
            print(f'exception find_by_document - {err}')
        return False
    @classmethod
    def find_by_unique(cls, session, v_find):
        try:
            select = session.query(
                cls
            ).filter(
                or_(
                    Person.id == v_find,
                    Person.document == v_find
                )
            )
            return select.first()
        except Exception as err:
            print(f'exception find_by_document - {err}')
        return False
    

    def exists_address(self, zipcode, number):
        for address in self.address_data:
            if zipcode == address.zipcode and number == address.number:
                return True
        return False
    

    def exists_contact(self, type_id, value):
        for contact in self.contact_data:
            if type_id == contact.type_id and value == contact.value:
                return True
        return False
    

    def exists_document(self, type_id, number):
        for document in self.document_data:
            if type_id == document.type_id and number == document.number:
                return True
        return False
    
    def exists_custom(self, type_id, value):
        t_required = {}
        is_equal = False
        for custom in self.custom_data:
            if custom.type_id == type_id:
                sample = custom.CustomDataType.base
                is_equal = False
                for item in sample:
                    if sample[item].get('required', False) == True:
                        if item not in value.keys():
                            raise ValueError(f"CustomData.{type_id} needs {item}")
                        else:
                            if custom.value[item] == value.get(item):
                                if is_equal is False:
                                    is_equal = True
                            elif is_equal is True:
                                is_equal = False
                                break
                            else:
                                break
                if is_equal:
                    return True
        return False
                            

        # try:
        #     ttypes = CustomDataType.check_type_key(session=None, )
        #     required = globals()[type_id].schema()['required']
        #     if required:
        #         for requer in required:
        #             if requer in value.dict().keys():
        #                 t_required.update({
        #                     requer: getattr(value, requer)
        #                 })
        #             else:
        #                 raise ValueError(f"CustomData.{type_id} needs {requer}")
        # except ValueError as verr:
        #     raise verr
        # except Exception as err:
        #     print(f'exists custom exp - {err}')
        # if t_required:
        #     for custom in self.custom_data:
        #         if custom.type_id == type_id:
        #             is_equal = False
        #             for r in t_required:
        #                 print(f'kkk {r} ---- {custom.value[r]} --- {t_required[r]}')
        #                 if custom.value[r] == t_required[r]:
        #                     if is_equal is False:
        #                         is_equal = True
        #                 elif is_equal is True:
        #                     print(f'quebrou checando {r}')
        #                     is_equal = False
        #                     break
        #                     #return False
        #                 else:
        #                     break
        #             if is_equal:
        #                 return True
        # return False








class Person(CRUDPersonBase, Base):
    __tablename__ = 'Person'
    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False)
    birthday = Column(DateTime, nullable=False)
    person_id = Column(String(36), ForeignKey("GlobalPerson.id"), nullable=False)
    source_id = Column(String(36), ForeignKey("Source.id"), nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow())
    # address_data = relationship('Address', backref='Person')
    # contact_data = relationship('Contact', backref='Person')
    # document_data = relationship('Document', backref='Person')

    @classmethod
    def create(
        cls: Base,
        session: Session,
        data_item: PersonDataSchemaAdd
    ):
        data_person = GlobalPerson.check_global_person_exists(session=session, v_find=data_item.person_id)
        data_item.person_id = data_person.id
        if not data_item.source_id:
            data_item.source_id = data_person.source_id
        data = data_item.dict()
        return super().create(session, data)







class Person33333333333(CRUDPersonBase, Base):
    __tablename__ = 'Perso333n'
    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False)
    birthday = Column(DateTime, nullable=False)
    document = Column(String(11), nullable=False)
    source_id = Column(String(36), ForeignKey("Source.id"), nullable=False)
    #source_id = Column(String(36), ForeignKey('registro2.id'))
    #source_id = Column(String(36), nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow())
    #address_data = relationship('Address', backref='Person')
    #contact_data = relationship('Contact', backref='Person')
    # document_data = relationship('Document', backref='Person')


    @classmethod
    def create(
        cls: Base,
        session: Session,
        person_data: PersonSchemaAdd
    ):
        avoid = Source.check_source_exists(session=session, v_find=person_data.source_id)
        data_person = Person.find_by_unique(session=session, v_find=person_data.document)
        if not data_person:
            data_person = super().create(session, person_data.dict())
        else:
            data_person.source_id = person_data.source_id
        return data_person
    

    @classmethod
    def random_person(cls, session):
        try:
            return session.query(
                cls
            ).outerjoin(
                Contact,
                Address,
                Document
            ).order_by(
                func.random()
            ).limit(
                1
            ).first()
        except Exception as err:
            print(f'exception find_by_document - {err}')
        return False
        
    def exists_address(self, zipcode, number):
        for address in self.address_data:
            if zipcode == address.zipcode and number == address.number:
                return True
        return False
    

    def exists_contact(self, type_id, value):
        for contact in self.contact_data:
            if type_id == contact.type_id and value == contact.value:
                return True
        return False
    

    def exists_document(self, type_id, number):
        for document in self.document_data:
            if type_id == document.type_id and number == document.number:
                return True
        return False
    
    @classmethod
    def find_by_document(cls, session, document):
        try:
            return session.query(
                cls
            ).filter_by(
                document=document
            ).first()
        except Exception as err:
            print(f'exception find_by_document - {err}')
        return False
    @classmethod
    def list_all(
        cls: Base,
        session: Session
    ):
        try:
            return session.query(
                cls
            ).all()
        except Exception as err:
            print(f'exception find_by_name_like - {err}')
        return False
    @classmethod
    def find_by_person_fields(cls, session, v_find):
        try:
            select = session.query(
                cls
            ).outerjoin(
                Contact,
                Address,
                Document
            ).filter(
                or_(
                    Person.id == v_find,
                    Person.document == v_find,
                    Contact.value == v_find,
                    Document.number == v_find
                )
            )
            response = select.all()
            if response:
                return response    
        except Exception as err:
            print(f'exception find_by_document - {err}')
        raise ItemNotFound(message=f'didnt find any person with value --> {v_find}')
        return False
    @classmethod
    def find_by_unique(cls, session, v_find):
        try:
            select = session.query(
                cls
            ).filter(
                or_(
                    Person.id == v_find,
                    Person.document == v_find
                )
            )
            return select.first()
        except Exception as err:
            print(f'exception find_by_document - {err}')
        return False
    @classmethod
    def check_person_exists(cls, session, v_find):
        temp = Person.find_by_unique(session=session, v_find=v_find)
        if not temp:
            raise ItemNotFound(message=f'didnt find any person with value --> {v_find}')
        return temp
    @classmethod
    def list_by_id(
        cls: Base, 
        session: Session,
        person_data_id: PersonSchemaListById
    ):
        try:
            return session.query(
                cls
            ).filter_by(
                id=person_data_id.id
            ).first()
        except Exception as err:
            print(f'exception list_by_id - {err}')
        return False




class Address(CRUDByPersonBase, Base):
    __tablename__ = 'Address'
    id = Column(String(36), primary_key=True)
    description = Column(String(255), nullable=True, default=None)
    name = Column(String(120), nullable=True, default=None)
    prefix = Column(String(11), nullable=True, default=None)
    street = Column(String(255), nullable=True, default=None)
    neighborhood = Column(String(255), nullable=True, default=None)
    zipcode = Column(String(11), nullable=False)
    number = Column(String(11), nullable=True)
    complement = Column(String(255), nullable=True, default=None)
    city = Column(String(255), nullable=True, default=None)
    state = Column(String(255), nullable=True, default=None)
    source_id = Column(String(36), ForeignKey("Source.id"), nullable=False)
    person_id = Column(String(36), ForeignKey("GlobalPerson.id"), nullable=False)
    #global_id = Column(String(36), ForeignKey("GlobalPerson.id"), nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow())
    @classmethod
    def create(
        cls: Base,
        session: Session,
        data_item: AddressSchemaAddAPI
    ):
        data_person = GlobalPerson.check_global_person_exists(session=session, v_find=data_item.person_id)
        #data_person = Person.check_person_exists(session=session, v_find=data_item.person_id)
        data_item.person_id = data_person.id
        if not data_item.source_id:
            data_item.source_id = data_person.source_id
        data = data_item.dict()
        return super().create(session, data)

    def funcao_de_classe_pae(self):
        print('psiu')

    @classmethod
    def list_all(
        cls: Base,
        session: Session
    ):
        try:
            return session.query(
                cls
            ).all()
        except Exception as err:
            print(f'exception find_by_name_like - {err}')
        return False
    






class ContactType(CRUDPersonBase, Base):
    __tablename__ = 'ContactType'
    id = Column(String(36), primary_key=True)
    description = Column(String(255), nullable=False)
    key = Column(String(255), unique=True, nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow())
    contact_type_data = relationship('Contact', backref='ContactType')
    @classmethod
    def create(
        cls: Type[Base],
        session: Session,
        contact_type_data: ContactTypeSchemaAdd
    ):
        return super().create(session, contact_type_data.dict())
    @classmethod
    def check_type_key(cls, session, key):
        try:
            return session.query(cls).filter_by(key=key).one()
        except Exception as err:
            print(err)
            raise ItemNotFound(message=f'didnt find contact.type_id key --> {key}')
    @classmethod
    def __table_cls__(cls, metadata, *args, **kwargs):
        table = Table(cls.__tablename__, Base.metadata, *args)
        if not table.exists(engine):
            cls.it_exists = False
        else:
            cls.it_exists = True
        return table
    @classmethod
    def _after_create(cls, connection):
        temp = cls()
        if temp.it_exists == False:
            pre_keys = [
                {
                    'description': 'Telefone',
                    'key': 'phone'
                },
                {
                    'description': 'Celular',
                    'key': 'mobile'
                },
                {
                    'description': 'Email',
                    'key': 'email'
                },
            ]
            session = SessionLocal(bind=connection)
            seraveinho = []
            #session.begin()
            for contact in pre_keys:
                temp_2 = cls()
                temp_2.id = str(uuid.uuid4())
                temp_2.description = contact.get('description')
                temp_2.key = contact.get('key')
                temp_2.date_created = datetime.utcnow()
                seraveinho.append(temp_2)
                #session.add(temp)
            session.add_all(seraveinho)
            session.commit()
    @event.listens_for(Base.metadata, 'after_create')
    def receive_after_create(target, connection, **kw):
        try:
            t_table = kw.get('tables', [])
            if t_table:
                globals()[t_table[0].name]()._after_create(connection=connection)
        except Exception as err:
            print(f'contacttype receive after exp - {err}')





class Contact(CRUDByPersonBase, Base):
    __tablename__ = 'Contact'
    id = Column(String(36), primary_key=True)
    description = Column(String(255), nullable=True, default=None)
    type_id = Column(String(36), ForeignKey("ContactType.key"), nullable=False)
    #type = Column(String(255), nullable=False)
    name = Column(String(11), nullable=True)
    value = Column(String(255), nullable=False)
    #source_id = Column(String(36), nullable=False)
    source_id = Column(String(36), ForeignKey("Source.id"), nullable=False)
    #person_id = Column(String(36), nullable=False)
    person_id = Column(String(36), ForeignKey("GlobalPerson.id"), nullable=False)
    #global_id = Column(String(36), ForeignKey("GlobalPerson.id"), nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow())


    @classmethod
    def create(
        cls: Base,
        session: Session,
        data_item: ContactSchemaAddAPI
    ):
        data_person = GlobalPerson.check_global_person_exists(session=session, v_find=data_item.person_id)
        #data_person = Person.check_person_exists(session=session, v_find=data_item.person_id)
        data_item.person_id = data_person.id
        avoid = ContactType.check_type_key(session=session, key=data_item.type_id)
        if not data_item.source_id:
            data_item.source_id = data_person.source_id
        data = data_item.dict()
        return super().create(session, data)
        temp = Contact(**contact_data.dict())
        temp.id = str(uuid.uuid4())
        temp.date_created = datetime.utcnow()
        session.add(temp)
        session.commit()
        session.refresh(temp)
        return temp
    


    



class DocumentType(CRUDPersonBase, Base):
    __tablename__ = 'DocumentType'
    id = Column(String(36), primary_key=True)
    description = Column(String(255), nullable=False)
    key = Column(String(255), unique=True, nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow())
    document_type_data = relationship('Document', backref='DocumentType')
    @classmethod
    def create(
        cls: Type[Base],
        session: Session,
        data_document: DocumentTypeSchemaAdd
    ):
        return super().create(session, data_document.dict())
    @classmethod
    def check_type_key(cls, session, key):
        try:
            return session.query(cls).filter_by(key=key).one()
        except Exception as err:
            print(err)
            raise ItemNotFound(message=f'didnt find document.type_id key --> {key}')
    @classmethod
    def __table_cls__(cls, metadata, *args, **kwargs):
        table = Table(cls.__tablename__, Base.metadata, *args)
        if not table.exists(engine):
            cls.it_exists = False
        else:
            cls.it_exists = True
        return table
    @classmethod
    def _after_create(cls, connection):
        temp = cls()
        if temp.it_exists == False:
            pre_keys = [
                {
                    "description": "Registro Geral",
                    "key": "rg"
                },
                {
                    "description": "Cadastro de Pessoa Fisica",
                    "key": "cpf"
                }
            ]
            session = SessionLocal(bind=connection)
            itens = []
            for key in pre_keys:
                temp_doc = cls()
                temp_doc.id = str(uuid.uuid4())
                temp_doc.description = key['description']
                temp_doc.key = key['key']
                temp_doc.date_created = datetime.utcnow()
                itens.append(temp_doc)
            session.add_all(itens)
            session.commit()
    @event.listens_for(Base.metadata, 'after_create')
    def receive_after_create(target, connection, **kw):
        print(f'{target} - {connection} - {kw}')
        try:
            tabela = kw.get('tables', [])
            if tabela:
                for que_tu_eh in tabela:
                    print(f'\n\n\n{type(que_tu_eh)} ---- {que_tu_eh}\n\n\n')
                    globals()[que_tu_eh.name]()._after_create(connection=connection)
            #print(type(que_tu_eh.name))z
            # print(tabela.__class__)
            # print(dir(tabela))
            # tabela._after_create(connection=connection)
        except Exception as err:
            print(f'receive after exp - {err}')





class Document(CRUDByPersonBase, Base):
    __tablename__ = 'Document'
    id = Column(String(36), primary_key=True)
    type_id = Column(String(36), ForeignKey("DocumentType.key"), nullable=False)
    description = Column(String(255), nullable=True, default=None)
    date_issuing = Column(String(255), nullable=True)
    date_expiration = Column(String(255), nullable=True)
    state_issuing = Column(String(255), nullable=True)
    issuing_authority = Column(String(255), nullable=True)
    number = Column(String(255), nullable=False)
    source_id = Column(String(36), ForeignKey("Source.id"), nullable=False)
    person_id = Column(String(36), ForeignKey("GlobalPerson.id"), nullable=False)
    #global_id = Column(String(36), ForeignKey("GlobalPerson.id"), nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow())


    @classmethod
    def create(
        cls: Base,
        session: Session,
        data_item: DocumentSchemaAddAPI
    ):
        data_person = GlobalPerson.check_global_person_exists(session=session, v_find=data_item.person_id)
        data_item.person_id = data_person.id
        #data_item.global_id = data_person.id
        avoid = DocumentType.check_type_key(session=session, key=data_item.type_id)
        if not data_item.source_id:
            data_item.source_id = data_person.source_id
        data = data_item.dict()
        return super().create(session, data)






class CustomDataType(CRUDPersonBase, Base):
    __tablename__ = 'CustomDataType'
    id = Column(String(36), primary_key=True)
    description = Column(String(255), nullable=False)
    key = Column(String(255), unique=True, nullable=False)
    base = Column(JSON, nullable=False)##?????????????
    date_created = Column(DateTime, default=datetime.utcnow())
    customdata_type_data = relationship('CustomData', backref='CustomDataType')
    @classmethod
    def create(
        cls: Type[Base],
        session: Session,
        data_item: CustomDataTypeSchemaAdd
    ):
        return super().create(session, data_item.dict())
    
    @classmethod
    def check_type_key(cls, session, description, key):
        try:
            return session.query(cls).filter_by(key=key).one()
        except Exception as err:
            #return CustomDataType.create(session=session, data_item=CustomDataTypeSchemaAdd(description=description, key=key))
            print(err)
            raise ItemNotFound(message=f'didnt find CustomDataType.type_id key --> {key}')



class CustomData(CRUDByPersonBase, Base):
    __tablename__ = 'CustomData'
    id = Column(String(36), primary_key=True)
    type_id = Column(String(36), ForeignKey("CustomDataType.key"), nullable=False)
    description = Column(String(255), nullable=True, default=None)
    value = Column(JSON, nullable=False)
    source_id = Column(String(36), ForeignKey("Source.id"), nullable=False)
    person_id = Column(String(36), ForeignKey("GlobalPerson.id"), nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow())

    @classmethod
    def create(
        cls: Base,
        session: Session,
        data_item: CustomDataSchemaAddAPI
    ):
        data_person = GlobalPerson.check_global_person_exists(session=session, v_find=data_item.person_id)
        data_item.person_id = data_person.id
        avoid = CustomDataType.check_type_key(session=session, description=data_item.description, key=data_item.type_id)
        #check_custom_data = CustomData.exists_custom_data(session=session, person_id=data_person.id, type_id=data_item.type_id, value=data_item.value)
        #print(check_custom_data)
        check_custom_data = False
        if check_custom_data:
            raise ValueError("CustomData already exists for the person")
        if not data_item.source_id:
            data_item.source_id = data_person.source_id
        data = data_item.dict()
        return super().create(session, data)
    
    @classmethod
    def exists_custom_data(cls, session: Session, person_id: str, type_id: str, value: JSON) -> bool:
        t_required = {}
        try:
            required = globals()[type_id].schema()['required']
            if required:
                for requer in required:
                    if requer in value.dict().keys():
                        t_required.update({
                            requer: getattr(value, requer)
                        })
                    else:
                        raise ValueError(f"CustomData.{type_id} needs {requer}")
        except ValueError as verr:
            raise verr
        except Exception as err:
            print(f'exists custom exp - {err}')
        if t_required:
            select = session.query(
                CustomData
            ).filter_by(
                person_id=person_id,
                type_id=type_id
            )
            for item in t_required:
                print(f'{item} - {t_required[item]}')
                select = select.filter(
                    text(f'json_extract(value, "$.{item}") = "{t_required[item]}"')
                    #text(f'value[{item}] = "{t_required[item]}"')
                )
                #select = select.filter(
                #    CustomData.value[item] == t_required[item]
                #)
            aaa = select.first() is not None
            print(aaa)
            return aaa
        return False
        return session.query(cls).filter_by(person_id=person_id, type_id=type_id).first() is not None






