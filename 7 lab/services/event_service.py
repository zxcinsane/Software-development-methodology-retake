from typing import List
from models.event import Event
from repositories.event_repository import EventRepository


class EventService:
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    def get_all_events(self) -> List[Event]:
        return self.event_repository.get_all()

    def get_event_by_id(self, event_id: int) -> Event:
        return self.event_repository.get_by_id(event_id)

    def add_event(self, event: Event) -> None:
        self.event_repository.add(event)

    def update_event(self, event: Event) -> None:
        self.event_repository.update(event)
