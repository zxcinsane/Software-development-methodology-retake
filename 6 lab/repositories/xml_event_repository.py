from typing import List
from models.event import Event
from repositories.event_repository import EventRepository
from lxml import etree


class XmlEventRepository(EventRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def _get_next_id(self, events: List[Event]) -> int:
        if len(events) == 0:
            return 1
        else:
            return max(event.id for event in events) + 1

    def get_all(self) -> List[Event]:
        with open(self.file_path, "rb") as f:
            xml = f.read()
            root = etree.fromstring(xml)

        events = []
        for event_xml in root.xpath("//event"):
            event_dict = {key: value for key, value in event_xml.attrib.items()}
            event = Event.from_dict(event_dict)

            events.append(event)

        return events

    def get_by_id(self, event_id: int) -> Event:
        with open(self.file_path, "rb") as f:
            xml = f.read()
            root = etree.fromstring(xml)

        event_xml = root.xpath(f"//event[@id='{event_id}']")[0]
        return Event.from_dict(event_xml.attrib)

    def add(self, event: Event) -> None:
        with open(self.file_path, "rb") as f:
            xml = f.read()
            root = etree.fromstring(xml)

        events = []
        for event_xml in root.xpath("//event"):
            event_dict = {key: value for key, value in event_xml.attrib.items()}
            event = Event.from_dict(event_dict)

            events.append(event)

        event.id = self._get_next_id(events)
        event_xml = etree.Element("event", event.to_dict())
        event_xml.set("id", str(event.id))
        root.append(event_xml)

        with open(self.file_path, "wb") as f:
            f.write(etree.tostring(root, pretty_print=True))

    def update(self, event: Event) -> None:
        with open(self.file_path, "rb") as f:
            xml = f.read()
            root = etree.fromstring(xml)

        event_xml = root.xpath(f"//event[@id='{event.id}']")[0]
        for attr, value in event.to_dict().items():
            event_xml.set(attr, str(value))

        with open(self.file_path, "wb") as f:
            f.write(etree.tostring(root, pretty_print=True))

    def delete(self, event_id: int) -> None:
        with open(self.file_path, "rb") as f:
            xml = f.read()
            root = etree.fromstring(xml)

        event_xml = root.xpath(f"//event[@id='{event_id}']")[0]
        root.remove(event_xml)

        with open(self.file_path, "wb") as f:
            f.write(etree.tostring(root, pretty_print=True))
