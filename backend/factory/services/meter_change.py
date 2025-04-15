# backend/factory/services/meter_change.py

from backend.singleton.account_manager import AccountManager

class MeterChangeService:
    def process_request(self, user_id):
        account_manager = AccountManager()
        user = account_manager.get_user_by_user_id(user_id)
        
        service_request = {
            "type": "Meter Change",
            "status": "Pending"
        }
        user["services"].append(service_request)
        return "🔁 Meter change request submitted successfully!"
