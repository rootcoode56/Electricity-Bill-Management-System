# backend/observer/observer.py

from abc import ABC, abstractmethod

# --- Observer Interface ---
class Observer(ABC):
    @abstractmethod
    def update(self, message):
        pass

# --- Concrete Observer ---
class UserObserver(Observer):
    def __init__(self, user):
        self.user = user

    def update(self, message):
        self.user['notifications'].append(message)
        print(f"Notification sent to {self.user['name']}: {message}")

# --- Subject Interface ---
class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer):
        pass

    @abstractmethod
    def detach(self, observer: Observer):
        pass

    @abstractmethod
    def notify(self, message):
        pass

# --- Concrete Subject ---
class NotificationCenter(Subject):
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, message):
        for observer in self._observers:
            observer.update(message)
