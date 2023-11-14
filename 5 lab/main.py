from abc import ABC, abstractmethod
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import List

Base = declarative_base()
engine = create_engine('sqlite:///example.db')
Session = sessionmaker(bind=engine)


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    announcement = Column(String)
    description = Column(String)
    date = Column(String)
    place = Column(String)
    category = Column(String)


class IRepository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def delete(self, obj):
        pass

    @abstractmethod
    def update(self, obj):
        pass

    @abstractmethod
    def get(self, id):
        pass

    @abstractmethod
    def get_all(self):
        pass


class EventRepository(IRepository):
    def __init__(self, session):
        self.session = session

    def add(self, event: Event):
        self.session.add(event)
        self.session.commit()

    def delete(self, event: Event):
        self.session.delete(event)
        self.session.commit()

    def update(self, event: Event):
        self.session.merge(event)
        self.session.commit()

    def get(self, id: int) -> Event:
        return self.session.query(Event).get(id)

    def get_all(self) -> List[Event]:
        return self.session.query(Event).all()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    session = Session()
    event_repository = EventRepository(session)
    event_example = Event(title="Название события",
                          author="Вячеслав Прошин",
                          announcement="Очень крутое событие, обязательно к посещению",
                          description="На самом деле нет, вы были пойманы на ошибке",
                          date="04.06.2002",
                          place="ул. Академика Зелинского, д. 6",
                          category="Научная конференция")
    event_repository.add(event_example)
    session.close()
