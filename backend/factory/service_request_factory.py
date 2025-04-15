# backend/factory/service_factory.py

from abc import ABC, abstractmethod
from backend.singleton.account_manager import AccountManager

# --- Product Interface ---
class ServiceRequest(ABC):
    @abstractmethod
    def process_request(self, user_id):
        pass

# --- Concrete Products ---
class NewConnectionRequest(ServiceRequest):
    def process_request(self, user_id):
        return f"🔌 New connection request submitted by {user_id}."

class MeterChangeRequest(ServiceRequest):
    def process_request(self, user_id):
        return f"⚙️ Meter change request submitted by {user_id}."

class NameCorrectionRequest(ServiceRequest):
    def process_request(self, user_id):
        return f"📝 Name correction request submitted by {user_id}."

# --- Factory Interface ---
class ServiceFactory(ABC):
    @abstractmethod
    def create_service(self):
        pass

# --- Concrete Factories ---
class NewConnectionFactory(ServiceFactory):
    def create_service(self):
        return NewConnectionRequest()

class MeterChangeFactory(ServiceFactory):
    def create_service(self):
        return MeterChangeRequest()

class NameCorrectionFactory(ServiceFactory):
    def create_service(self):
        return NameCorrectionRequest()

# --- Application Layer ---
class ServiceApplicationHandler:
    def __init__(self):
        self.account_manager = AccountManager()

    def apply_for_service(self, user_id, service_type):
        factory_map = {
            "new_connection": NewConnectionFactory(),
            "meter_change": MeterChangeFactory(),
            "name_correction": NameCorrectionFactory()
        }

        if service_type not in factory_map:
            return f"❌ Invalid service type: {service_type}"

        service = factory_map[service_type].create_service()
        user = self.account_manager.get_user_by_user_id(user_id)
        user['services'].append(service_type)
        return service.process_request(user_id)
