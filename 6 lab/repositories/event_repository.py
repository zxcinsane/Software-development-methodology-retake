from abc import ABC, abstractmethod
from typing import List
from models.event import Event


class EventRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Event]:
        pass

    @abstractmethod
    def get_by_id(self, event_id: int) -> Event:
        pass

    @abstractmethod
    def add(self, event: Event) -> None:
        pass

    @abstractmethod
    def update(self, event: Event) -> None:
        pass
