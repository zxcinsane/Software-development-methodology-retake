from dataclasses import dataclass
from typing import List
import uuid
import unittest


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
    event_id = len(EventRepository().events) + 1
    event = Event(event_id, title, author, announcement, description, date, place, photo, category, feedback)
    EventRepository().save(event)
    return event


class EventRepository:
    def __init__(self):
        self.events = {}

    def save(self, event):
        self.events[event.event_id] = event

    def get(self, event_id):
        return self.events.get(event_id)


class UserRepository:
    def __init__(self):
        self.users = {}

    def save(self, user):
        self.users[user.user_id] = user

    def get(self, user_id):
        return self.users.get(user_id)


class TestEvent(unittest.TestCase):
    def test_create_event(self):
        test_category = Category(100, "Test category", "Test description")
        test_group = Group(100, "Test group", True, True, False)
        test_user = User(100, "Testing Subject", "test@gmail.com", test_group)
        event = Event(100, "Test event", test_user, "Test announcement", "Test description", "04.06.2022", "Test place", "Test photo", test_category, [])

        self.assertIsNotNone(event.event_id)
        self.assertIsInstance(event.event_id, str)
        self.assertEqual(len(event.event_id), 1)


class TestUser(unittest.TestCase):
    def test_create_user(self):
        test_group = Group(100, "Test group", True, True, False)
        user = User(100, "Testing Subject", "test@gmail.com", test_group)
        self.assertIsNotNone(user.user_id)
        self.assertEqual(user.name, "Testing Subject")
        self.assertEqual(user.email, "test@gmail.com")


class TestEventRepository(unittest.TestCase):
    def test_save_and_get_event(self):
        repository = EventRepository()
        test_category = Category(100, "Test category", "Test description")
        test_group = Group(100, "Test group", True, True, False)
        test_user = User(100, "Testing Subject", "test@gmail.com", test_group)
        event = Event(100, "Test event", test_user, "Test announcement", "Test description", "04.06.2022", "Test place", "Test photo", test_category, [])
        repository.save(event)

        saved_event = repository.get(event.event_id)
        self.assertEqual(saved_event, event)

    def test_get_nonexistent_event(self):
        repository = EventRepository()

        nonexistent_event = repository.get(str(uuid.uuid4()))
        self.assertIsNone(nonexistent_event)


class TestUserRepository(unittest.TestCase):
    def test_save_and_get_event(self):
        repository = UserRepository()
        test_group = Group(100, "Test group", True, True, False)
        user = User(100, "Testing Subject", "test@gmail.com", test_group)
        repository.save(user)

        saved_event = repository.get(user.user_id)
        self.assertEqual(saved_event, user)

    def test_get_nonexistent_user(self):
        repository = UserRepository()

        nonexistent_user = repository.get(str(uuid.uuid4()))
        self.assertIsNone(nonexistent_user)


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


if __name__ == "__main__":
    event_repository = EventRepository()
    user_repository = UserRepository()

    test_category = Category(100, "Test category", "Test description")
    test_group = Group(100, "Test group", True, True, False)
    user = User(100, "Testing Subject", "test@gmail.com", test_group)
    event = Event(100, "Test event", user, "Test announcement", "Test description", "04.06.2022", "Test place", "Test photo", test_category, [])

    event_repository.save(event)
    user_repository.save(user)

    saved_event = event_repository.get(event.event_id)
    saved_user = user_repository.get(user.user_id)

    if saved_event:
        print("Saved event:")
        print(f"ID: {saved_event.event_id}")
        print(f"Event title: {saved_event.title}")
        print(f"Event description: {saved_event.description}")
    else:
        print("Event not found in repository.")

    if saved_user:
        print("Saved user:")
        print(f"ID: {saved_user.user_id}")
        print(f"User name: {saved_user.name}")
        print(f"User email: {saved_user.email}")
    else:
        print("User not found in repository.")
