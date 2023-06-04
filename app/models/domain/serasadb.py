from sqlalchemy import(
    Column,
    Integer,
    String,
    ForeignKey,
    text,
    and_
)
from sqlalchemy.orm import Session
from sqlalchemy.types import(
    Date,
    Boolean,
    Time,
    DateTime
)

from app.core.database import Base                      
from datetime import datetime

from app.exceptions.serasadb_exceptions import(
    NoNameGivenError
)




class serasaData(Base):
    __tablename__ = "serasa"
    cpf = Column(String, primary_key=True)
    name = Column(String)
    genre = Column(String)
    birth = Column(String)
    birth_date = Column(Date)
    @classmethod
    def find_by_cpf(cls, session, cpf):
        try:
            return session.query(
                cls
            ).filter_by(
                cpf=cpf
            ).first()
        except Exception as err:
            print(f'exception find_by_cpf - {err}')
        return False
    @classmethod
    def find_by_name_like(cls, session, name_like):
        try:
            return session.query(
                cls
            ).filter(
                and_(
                    text("lower(name) like :name")
                )
            ).params(
                name=f'{name_like.lower()}%'
            ).all()
        except Exception as err:
            print(f'exception find_by_name_like - {err}')
        return False
    @staticmethod
    def deal_name(
        first_name: str = '',
        middle_name: str = '',
        last_name: str = ''
    ):
        name = ''
        last_char = ''
        if first_name:
            first_name = first_name.lower()
            name += f'{first_name}%'
            last_char = '%'
        if middle_name:
            start_char = '%'
            if last_char:
                start_char = ''
            else:
                last_char = '%'
            middle_name = middle_name.lower()
            name += f'{start_char}{middle_name}%'
        if last_name:
            start_char = '%'
            if last_char:
                start_char = ''
            last_name = last_name.lower()
            name += f'{start_char}{last_name}'
        return name
    @classmethod
    def find_by_partial_name(
        cls: Base,
        session: Session,
        first_name: str = '',
        middle_name: str = '',
        last_name: str = '',
        birth_day: int = 0,
        birth_month: int = 0,
        birth_year: int = 0,
        limit: int = 50
    ):
        if not first_name and not middle_name and not last_name:
            raise NoNameGivenError('no part name given')
        else:
            name = serasaData.deal_name(
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name
            )
            try:
                select = session.query(
                    cls
                ).filter(
                    text("lower(name) like :name")
                )
                params = {}
                #params = {"name": name}
                if birth_day:
                    select = select.filter(
                        text("extract(day from to_date(birth, 'DD/MM/YYYY')) = :day")
                    )
                    params.update({
                        'day': birth_day
                    })
                if birth_month:
                    select = select.filter(
                        text("extract(month from to_date(birth, 'DD/MM/YYYY')) = :month")
                    )
                    params.update({
                        'month': birth_month
                    })
                if birth_year:
                    select = select.filter(
                        text("extract(year from to_date(birth, 'DD/MM/YYYY')) = :year")
                    )
                    params.update({
                        'year': birth_year
                    })
                select = select.filter(
                    text("birth ~ '^[0-9]{2}/[0-9]{2}/[0-9]{4}$'")
                )
                query = select.params(name=name, **params)
                return query.limit(limit).all()
            except Exception as err:
                print(f'exception find_by_name_like - {err}')
        return False



