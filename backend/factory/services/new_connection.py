# backend/factory/services/new_connection.py

from backend.singleton.account_manager import AccountManager

class NewConnectionService:
    
        def process_request(self, user_id, connection_data):
            account_manager = AccountManager()
            user = account_manager.get_user_by_user_id(user_id)
            
            if not user:
                return "❌ User not found"
            
            if not connection_data.get("name") or not connection_data.get("address"):
                return "❌ Missing required connection data (name, address)"
            
            service_request = {
                "type": "New Connection",
                "status": "Pending",
                "connection_details": connection_data
            }
            
            user["services"].append(service_request)

            # No need to save, since it's already updated in memory
            return "📥 New connection request submitted successfully!"
