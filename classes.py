from datetime import datetime


class User:

    def __init__(self, name: str, email: str, password: int):
        self.name = name
        self.email = email
        self.password = password
        self.task = []

    def to_dict(self):
        return {
            "username": self.name,
            "password": self.password,
            "tasks": self.task,
        }


class Task:

    def __init__(self, title, description, category,  due_date, priority):

        self.title = title
        self.description = description
        self.category = category
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.due_date = due_date
        self.priority = priority
        self.status = "Pending"

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "created_at": self.created_at,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status,
        }
