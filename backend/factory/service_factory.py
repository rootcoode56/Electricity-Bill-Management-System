# backend/factory/service_factory.py

from backend.factory.services.new_connection import NewConnectionService
from backend.factory.services.meter_change import MeterChangeService
from backend.factory.services.name_change import NameChangeService

class ServiceApplicationHandler:
    
    def apply_for_service(self, user_id, service_type, connection_data=None):
        """
        This method processes service requests based on the service type.

        :param user_id: The ID of the user applying for the service.
        :param service_type: The type of service the user is applying for (new_connection, meter_change, etc.).
        :param connection_data: Additional data required for certain services (e.g., connection details for new_connection).
        :return: A response indicating the success or failure of the service request.
        """
        if service_type == "new_connection":
            # Create a service handler for the new connection service
            service = NewConnectionService()
            # Pass the connection data (for new connection service) and process the request
            return service.process_request(user_id, connection_data)
        
        elif service_type == "meter_change":
            # Process meter change service
            service = MeterChangeService()
            return service.process_request(user_id)
        
        elif service_type == "name_correction":
            # Process name change service
            service = NameChangeService()
            return service.process_request(user_id)
        
        else:
            # If an invalid service type is provided
            return "❌ Invalid service type"

