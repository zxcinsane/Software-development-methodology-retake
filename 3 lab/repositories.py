from abc import ABC, abstractmethod
from sqlalchemy import text
import models
from models import *


class AbstractRepository(ABC):
    @abstractmethod
    def get_by_id(self, obj_id: int):
        pass

    @abstractmethod
    def get_all(self) -> List:
        pass

    @abstractmethod
    def add(self, item):
        pass

    @abstractmethod
    def delete(self, obj_id: int):
        pass


class GroupRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def get_by_id(self, obj_id: int) -> Group:
        return self.session.query(models.Group).filter_by(id=obj_id).first()

    def get_all(self) -> List[Group]:
        return self.session.query(Group).all()

    def add(self, group: Group):
        if self.get_by_id(group.group_id) is None:
            self.session.execute(text(f"INSERT INTO groups (id, title, create_rights, delete_rights, admin_access) VALUES ('{group.group_id}', '{group.title}', '{group.create_rights}', '{group.delete_rights}', '{group.admin_access}')"))
            self.session.commit()

    def delete(self, obj_id: int):
        group = self.get_by_id(obj_id)
        if group is not None:
            self.session.delete(group)
            self.session.commit()


class CategoryRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def get_by_id(self, obj_id: int) -> Category:
        return self.session.query(models.Category).filter_by(id=obj_id).first()

    def get_all(self) -> List[Category]:
        return self.session.query(Category).all()

    def add(self, category: Category):
        if self.get_by_id(category.category_id) is None:
            self.session.execute(text(f"INSERT INTO categories (id, title, description) VALUES ('{category.category_id}', '{category.title}', '{category.description}')"))
            self.session.commit()

    def delete(self, obj_id: int):
        category = self.get_by_id(obj_id)
        if category is not None:
            self.session.delete(category)
            self.session.commit()


class UserRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def get_by_id(self, obj_id: int) -> User:
        return self.session.query(models.User).filter_by(id=obj_id).first()

    def get_all(self) -> List[User]:
        return self.session.query(User).all()

    def add(self, user: User):
        if self.get_by_id(user.user_id) is None:
            self.session.execute(text(f"INSERT INTO users (id, name, email, group) VALUES ('{user.user_id}', '{user.name}', '{user.email}', '{user.group.group_id}')"))
            self.session.commit()

    def delete(self, obj_id: int):
        user = self.get_by_id(obj_id)
        if user is not None:
            self.session.delete(user)
            self.session.commit()


class EventRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def get_by_id(self, obj_id: int) -> Event:
        return self.session.query(models.Event).filter_by(id=obj_id).first()

    def get_all(self) -> List[Event]:
        return self.session.query(Event).all()

    def add(self, event: Event):
        if self.get_by_id(event.event_id) is None:
            self.session.execute(text(f"INSERT INTO events (id, title, author, announcement, description, date, place, category) VALUES ('{event.event_id}', '{event.title}', '{event.author.user_id}', '{event.announcement}', '{event.description}', '{event.date}', '{event.place}', '{event.category.category_id}')"))
            self.session.commit()

    def delete(self, obj_id: int):
        event = self.get_by_id(obj_id)
        if event is not None:
            self.session.delete(event)
            self.session.commit()


class CommentRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def get_by_id(self, obj_id: int) -> Comment:
        return self.session.query(models.Comment).filter_by(id=obj_id).first()

    def get_all(self) -> List[Comment]:
        return self.session.query(Comment).all()

    def add(self, comment: Comment):
        if self.get_by_id(comment.comment_id) is None:
            self.session.execute(text(
                f"INSERT INTO comments (id, author, date, text) VALUES ('{comment.comment_id}', '{comment.author.user_id}', '{comment.date}', '{comment.text}')"))
            self.session.commit()

    def delete(self, obj_id: int):
        comment = self.get_by_id(obj_id)
        if comment is not None:
            self.session.delete(comment)
            self.session.commit()
