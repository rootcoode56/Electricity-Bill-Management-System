# backend/factory/services/name_change.py

from backend.singleton.account_manager import AccountManager

class NameChangeService:
    def process_request(self, user_id):
        account_manager = AccountManager()
        user = account_manager.get_user_by_user_id(user_id)
        
        service_request = {
            "type": "Name Correction",
            "status": "Pending"
        }
        user["services"].append(service_request)
        return "✏️ Name correction request submitted successfully!"
