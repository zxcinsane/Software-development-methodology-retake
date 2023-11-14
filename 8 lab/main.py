import asyncio
import json
import xml.etree.ElementTree as ET
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import List


Base = declarative_base()
engine = create_engine('sqlite:///example.db')
Session = sessionmaker(bind=engine)


class Event:
    def __init__(self, title, description, place):
        self.title = title
        self.description = description
        self.place = place

    def to_dict(self):
        return {"title": self.title, "description": self.description, "place": self.place}


class Repository:
    def save(self, data):
        raise NotImplementedError

    def load(self):
        raise NotImplementedError


class RelationalRepository(Repository):
    def __init__(self, session):
        self.session = session

    def save(self, data):
        self.session.add(data)
        self.session.commit()
        print("\n[сохранение в реляционной базе данных]: ", data)

    def load(self) -> List[Event]:
        print("\nзагрузка из реляционной базы данных...")
        return self.session.query(Event).all()


class XMLRepository(Repository):
    def save(self, data):
        root = ET.Element("events")
        for item in data:
            events_elem = ET.SubElement(root, "events")
            title_elem = ET.SubElement(events_elem, "title")
            title_elem.text = item["title"]
            description_elem = ET.SubElement(events_elem, "description")
            description_elem.text = item["description"]
            place_elem = ET.SubElement(events_elem, "place")
            place_elem.text = item["place"]

        tree = ET.ElementTree(root)
        tree.write("events.xml")

        print("\n[сохранение в XML]: ", data)

    def load(self):
        tree = ET.parse("events.xml")
        root = tree.getroot()

        events = []
        for event_elem in root.findall("event"):
            title_elem = event_elem.find("title")
            description_elem = event_elem.find("description")
            place_elem = event_elem.find("place")
            event = Event(title_elem.text, description_elem.text, place_elem.text)
            events.append(event)

        print("\nзагрузка из XML...")
        return events


class JSONRepository(Repository):
    def save(self, data):
        with open("events.json", "w") as file:
            json.dump(data, file, indent=4)

        print("\n[сохранение в JSON]: ", data)

    def load(self):
        with open("events.json", "r") as file:
            data = json.load(file)

        events = []
        for item in data:
            event = Event(item["title"], item["description"], item["place"])
            events.append(event)

        print("\nзагрузка из JSON...")
        return events


class RepositoryFactory:
    @staticmethod
    def create_repository(storage_type):
        if storage_type == 'relational':
            session = Session()
            return RelationalRepository(session)
        elif storage_type == 'xml':
            return XMLRepository()
        elif storage_type == 'json':
            return JSONRepository()
        else:
            raise ValueError("\n[ошибка при создании]")


class Wishlist:
    def __init__(self, repository):
        self.repository = repository
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def remove_event(self, event):
        self.events.remove(event)

    def display_list(self):
        print("\n[список желаемого]:\n")
        for event in self.events:
            print(f"[название]: {event.title}, \n[описание]: {event.description}, \n[место проведения]: {event.place}\n")

    async def save_list(self):
        print("\nИмпорт списка...")
        await asyncio.sleep(1)
        self.repository.save([event.to_dict() for event in self.events])
        print("Список желаемого сохранен")


def test_repository_factory():
    factory = RepositoryFactory()

    repository_relational = factory.create_repository('relational')
    assert isinstance(repository_relational, RelationalRepository)

    repository_xml = factory.create_repository('xml')
    assert isinstance(repository_xml, XMLRepository)

    repository_json = factory.create_repository('json')
    assert isinstance(repository_json, JSONRepository)

    print("\n[тест фабрики]: успешно")


async def test_coroutines(storage_type):
    factory = RepositoryFactory()
    repository = factory.create_repository(storage_type)
    list = Wishlist(repository)

    event = Event("Событие", "Это событие крутое", "На улице")
    also_event = Event("Тоже событие", "А это не очень", "В помещении")
    list.add_event(event)
    list.add_event(also_event)

    list.display_list()
    await list.save_list()

    loaded_events = repository.load()
    for event in loaded_events:
        print(f"\n[событие загружено]: {event.title}, {event.description}, {event.place}")

    print("\n[тест корутинов]: успешно")

test_repository_factory()
storage_type = input("\n[выберите тип создаваемого хранилища]:\n> xml\n> json\n> relational\n\n[]: ")
asyncio.run(test_coroutines(storage_type))
