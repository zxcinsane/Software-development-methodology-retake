from sqlalchemy import Column, Integer, String, ForeignKey, Table, MetaData, Boolean
from sqlalchemy.orm import registry
import models

metadata = MetaData()
mapper_registry = registry()

groups = Table('groups', metadata,
               Column('id', Integer, primary_key=True, autoincrement=False),
               Column('title', String),
               Column('create_rights', Boolean, default=False),
               Column('delete_rights', Boolean, default=False),
               Column('admin_access', Boolean, default=False)
               )

categories = Table('categories', metadata,
                   Column('id', Integer, primary_key=True, autoincrement=False),
                   Column('title', String),
                   Column('description', String)
                   )

users = Table('users', metadata,
              Column('id', Integer, primary_key=True, autoincrement=False),
              Column('name', String),
              Column('email', String),
              Column('group', Integer, ForeignKey('groups.id'))
              )

events = Table('events', metadata,
               Column('id', Integer, primary_key=True, autoincrement=False),
               Column('title', String),
               Column('author', Integer, ForeignKey('users.id')),
               Column('announcement', String),
               Column('description', String),
               Column('date', String),
               Column('place', String),
               Column('category', Integer, ForeignKey('categories.id'))
               )

comments = Table('comments', metadata,
                 Column('id', Integer, primary_key=True, autoincrement=False),
                 Column('author', Integer, ForeignKey('users.id')),
                 Column('date', String),
                 Column('text', String),
                 )


def start_mappers():
    mapper_registry.map_imperatively(models.Group, groups)
    mapper_registry.map_imperatively(models.Category, categories)
    mapper_registry.map_imperatively(models.User, users)
    mapper_registry.map_imperatively(models.Event, events)
    mapper_registry.map_imperatively(models.Comment, comments)
