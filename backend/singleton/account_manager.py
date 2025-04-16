from backend.utils.mock_data import get_mock_data
from backend.observer.observer import NotificationCenter, UserObserver

class AccountManager:
    _instance = None

    def __new__(cls):
        """
        Singleton pattern to ensure only one instance of AccountManager is created.
        Loads users from mock data and initializes notification center.
        """
        if cls._instance is None:
            cls._instance = super(AccountManager, cls).__new__(cls)
            cls._instance.users = get_mock_data()  # Dict keyed by user_id
            cls._instance.notification_center = NotificationCenter()

            # Ensure all users have notifications list and observer attached
            for user in cls._instance.users.values():
                if 'notifications' not in user:
                    user['notifications'] = []
                cls._instance.notification_center.attach(UserObserver(user))

        return cls._instance

    def authenticate(self, username, password):
        """
        Authenticates a user by matching username and password.
        Returns user_id if successful, None otherwise.
        """
        user = next((u for u in self.users.values() if u['username'] == username and u['password'] == password), None)
        if user:
            if 'notifications' not in user:
                user['notifications'] = []
                self.notification_center.attach(UserObserver(user))
            return user['user_id']
        return None

    def get_user_by_user_id(self, user_id):
        """
        Retrieves a user by their user_id and ensures notification support.
        """
        user = self.users.get(user_id)
        if user and 'notifications' not in user:
            user['notifications'] = []
            self.notification_center.attach(UserObserver(user))
        return user

    def get_user_by_meter_id(self, meter_id):
        """
        Retrieves a user by their meter_id and ensures notification support.
        Supports search strategy (SearchByMeterID).
        """
        user = next((u for u in self.users.values() if u.get('meter_id') == meter_id), None)
        if user and 'notifications' not in user:
            user['notifications'] = []
            self.notification_center.attach(UserObserver(user))
        return user

    def notify_user(self, user_id, message):
        """
        Sends a notification to the user using observer pattern.
        """
        user = self.get_user_by_user_id(user_id)
        if user:
            self.notification_center.notify(message)

    def add_user(self, user_id, username, password, name, address, role="customer", meter_id=None):
        """
        Adds a new user with notification observer attached.
        """
        if user_id in self.users:
            raise ValueError(f"User ID {user_id} already exists.")

        new_user = {
            "user_id": user_id,
            "username": username,
            "password": password,
            "name": name,
            "address": address,
            "role": role,
            "meter_id": meter_id,
            "bills": [],
            "notifications": [],
            "complaints": [],
            "services": []
        }
        self.users[user_id] = new_user
        self.notification_center.attach(UserObserver(new_user))
        return new_user

    def get_user_role(self, user_id):
        """
        Returns the role of a user (e.g., 'admin' or 'customer').
        """
        user = self.get_user_by_user_id(user_id)
        return user.get("role") if user else None

    def update_user(self, user_id, **kwargs):
        """
        Updates user information with provided keyword arguments.
        """
        user = self.get_user_by_user_id(user_id)
        if not user:
            raise ValueError("User not found.")

        valid_fields = ["username", "password", "name", "address", "role", "meter_id", "bills", "notifications", "complaints", "services"]
        for key, value in kwargs.items():
            if key in valid_fields:
                user[key] = value
            else:
                raise ValueError(f"Invalid field: {key}")

        self.users[user_id] = user
        return user

    def save_user(self, user):
        """
        Saves a user to the users dictionary (used by services like NewConnectionService).
        """
        if user['user_id'] not in self.users:
            raise ValueError(f"User ID {user['user_id']} does not exist.")
        self.users[user['user_id']] = user