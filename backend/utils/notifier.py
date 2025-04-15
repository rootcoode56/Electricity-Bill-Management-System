# notifier.py

from observer.subject import Subject
from observer.observer import Observer

class Notifier:
    def __init__(self):
        self.subject = Subject()

    def add_observer(self, observer):
        """Adds an observer to the notification system."""
        self.subject.register(observer)

    def remove_observer(self, observer):
        """Removes an observer from the notification system."""
        self.subject.remove(observer)

    def send_notification(self, message):
        """Sends a notification to all observers."""
        self.subject.notify(message)
