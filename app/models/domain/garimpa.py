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
    DateTime
)
from typing import List, Type, Union

from sqlalchemy.orm import relationship

from app.core.database import Base, engine, SessionLocal         
from datetime import datetime

from app.exceptions.serasadb_exceptions import(
    NoNameGivenError
)

from app.exceptions.person_exceptions import(
    PersonNotFound
)


from app.exceptions.garimpa_exceptions import(
    ItemNotFound
)



from app.models.schemas.garimpa import(
    SourceSchemaAdd,
    PersonSchemaAdd,
    AddressSchemaAdd,
    AddressSchemaAddAPI,
    ContactSchemaAdd,
    ContactSchemaAddAPI,
    DocumentTypeSchemaAdd,
    DocumentSchemaAddAPI,
    DocumentSchemaAdd,
    PersonSchemaListById,
    ContactTypeSchemaAdd,
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






class GlobalPerson(CRUDPersonBase, Base):
    __tablename__ = "GlobalPerson"
    id = Column(String(36), primary_key=True)
    date_created = Column(DateTime, default=datetime.utcnow)
    










class Source(CRUDPersonBase, Base):
    __tablename__ = 'Source'
    id = Column(String(36), primary_key=True)
    description = Column(String(255), nullable=False)
    author = Column(String(120), nullable=True, default=None)
    date = Column(DateTime, nullable=True, default=None)
    date_created = Column(DateTime, default=datetime.utcnow())
    source_data = relationship('Person', backref='Source')
    source_address = relationship('Address', backref='Source')
    source_contact = relationship('Contact', backref='Source')
    source_document = relationship('Document', backref='Source')
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
            raise ItemNotFound(message=f'didnt find source with value --> {v_find}')
        return temp
        




class Person(CRUDPersonBase, Base):
    __tablename__ = 'Person'
    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False)
    birthday = Column(String(120), nullable=False)
    document = Column(String(11), nullable=False)
    source_id = Column(String(36), ForeignKey("Source.id"), nullable=False)
    #source_id = Column(String(36), ForeignKey('registro2.id'))
    #source_id = Column(String(36), nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow())
    address_data = relationship('Address', backref='Person')
    contact_data = relationship('Contact', backref='Person')
    document_data = relationship('Document', backref='Person')


    @classmethod
    def create(
        cls: Base,
        session: Session,
        person_data: PersonSchemaAdd
    ):
        avoid = Source.check_source_exists(session=session, v_find=person_data.source_id)
        data = person_data.dict()
        return super().create(session, data)
    

    
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
            #).filter_by(
            #    document=document
            #)
            response = select.all()
            if response:
                return response    
        except Exception as err:
            print(f'exception find_by_document - {err}')
        raise ItemNotFound(message=f'didnt find person with value --> {v_find}')
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
            #).filter_by(
            #    document=document
            #)
            return select.first()
        except Exception as err:
            print(f'exception find_by_document - {err}')
        return False
    @classmethod
    def check_person_exists(cls, session, v_find):
        temp = Person.find_by_unique(session=session, v_find=v_find)
        if not temp:
            raise ItemNotFound(message=f'didnt find person with value --> {v_find}')
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
    #source_id = Column(String(36), nullable=False)
    person_id = Column(String(36), ForeignKey("Person.id"), nullable=False)
    #person_id = Column(String(36), nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow())
    @classmethod
    def create(
        cls: Base,
        session: Session,
        data_item: AddressSchemaAddAPI
    ):
        data_person = Person.check_person_exists(session=session, v_find=data_item.person_id)
        data_item.person_id = data_person.id
        if not data_item.source_id:
            data_item.source_id = data_person.source_id
        data = data_item.dict()
        return super().create(session, data)



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
    person_id = Column(String(36), ForeignKey("Person.id"), nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow())


    @classmethod
    def create(
        cls: Base,
        session: Session,
        data_item: ContactSchemaAddAPI
    ):
        data_person = Person.check_person_exists(session=session, v_find=data_item.person_id)
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
    #source_id = Column(String(36), nullable=False)
    #person_id = Column(String(36), nullable=False)
    source_id = Column(String(36), ForeignKey("Source.id"), nullable=False)
    person_id = Column(String(36), ForeignKey("Person.id"), nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow())
    # @classmethod
    # def create(
    #     cls: Base,
    #     session: Session,
    #     data: DocumentSchemaAdd
    # ):
    #     temp = Document(**data.dict())
    #     temp.id = str(uuid.uuid4())
    #     temp.date_created = datetime.utcnow()
    #     session.add(temp)
    #     session.commit()
    #     session.refresh(temp)
    #     return temp
    @classmethod
    def create(
        cls: Base,
        session: Session,
        data_item: DocumentSchemaAddAPI
    ):
        data_person = Person.check_person_exists(session=session, v_find=data_item.person_id)
        data_item.person_id = data_person.id
        avoid = DocumentType.check_type_key(session=session, key=data_item.type_id)
        if not data_item.source_id:
            data_item.source_id = data_person.source_id
        data = data_item.dict()
        return super().create(session, data)









   

