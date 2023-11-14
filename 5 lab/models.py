from dataclasses import dataclass
from typing import List
import uuid


class Category:
    def __init__(self, category_id: int, title: str, description: str):
        self.category_id = category_id
        self.title = title
        self.description = description

    def __eq__(self, other):
        if not isinstance(other, Category):
            return False
        return (self.category_id == other.category_id and
                self.title == other.title and
                self.description == other.description)


class Group:
    def __init__(self, group_id: int, title: str, create_rights: bool, delete_rights: bool, admin_access: bool):
        self.group_id = group_id
        self.title = title
        self.create_rights = create_rights
        self.delete_rights = delete_rights
        self.admin_access = admin_access

    def __eq__(self, other):
        if not isinstance(other, Group):
            return False
        return (self.group_id == other.group_id and
                self.title == other.title and
                self.create_rights == other.create_rights and
                self.delete_rights == other.delete_rights and
                self.admin_access == other.admin_access)


class User:
    def __init__(self, user_id: int, name: str, email: str, group: Group):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.group = group
        self.wishlist: List[Event] = []
        self.favourite_category: List[Category] = []

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return (self.user_id == other.user_id and
                self.name == other.name and
                self.email == other.email and
                self.group == other.group and
                self.wishlist == other.wishlist and
                self.favourite_category == other.favourite_category)

    def add_category(self, category: Category):
        if category not in self.favourite_category:
            self.favourite_category.append(category)

    def remove_category(self, category: Category):
        if category in self.favourite_category:
            self.favourite_category.remove(category)


class Comment:
    def __init__(self, comment_id: int, author: User, date: str, text: str):
        self.comment_id = comment_id
        self.author = author
        self.date = date
        self.text = text

    def __eq__(self, other):
        if not isinstance(other, Comment):
            return False
        return (self.comment_id == other.comment_id and
                self.author == other.author and
                self.date == other.date and
                self.text == other.text)


@dataclass(frozen=True)
class Event:
    event_id: int
    title: str
    author: User
    announcement: str
    description: str
    date: str
    place: str
    photo: str
    category: Category
    feedback: List[Comment]

    def __eq__(self, other):
        return (self.event_id == other.event_id and
                self.title == other.title and
                self.author == other.author and
                self.announcement == other.announcement and
                self.description == other.description and
                self.date == other.date and
                self.place == other.place and
                self.photo == other.photo and
                self.category == other.category and
                self.feedback == other.feedback)


def create_user(name: str, email: str, group: Group) -> User:
    user_id = int(uuid.uuid4())
    user = User(user_id, name, email, group)
    return user


def create_event(title: str, author: User, announcement: str, description: str, date: str, place: str, photo: str, category: Category) -> Event:
    feedback = []
    event_id = int(uuid.uuid4())
    event = Event(event_id, title, author, announcement, description, date, place, photo, category, feedback)
    return event


def create_comment(author: User, date: str, text: str, event: Event):
    comment_id = int(uuid.uuid4())
    comment = Comment(comment_id, author, date, text)
    event.feedback.append(comment)


def create_group(title: str, create_rights: bool, delete_rights: bool, admin_access: bool) -> Group:
    group_id = int(uuid.uuid4())
    group = Group(group_id, title, create_rights, delete_rights, admin_access)
    return group


def create_category(title: str, description: str) -> Category:
    category_id = int(uuid.uuid4())
    category = Category(category_id, title, description)
    return category
