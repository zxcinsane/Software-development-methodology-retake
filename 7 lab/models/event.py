class Event:
    def __init__(self, title, author, announcement, description, date, place, category):
        self.title = title
        self.author = author
        self.announcement = announcement
        self.description = description
        self.date = date
        self.place = place
        self.category = category

    @classmethod
    def from_dict(cls, dict):
        return cls(**dict)

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "announcement": self.announcement,
            "description": self.description,
            "date": self.date,
            "place": self.place,
            "category": self.category
        }

