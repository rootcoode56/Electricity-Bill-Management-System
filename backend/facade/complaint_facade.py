from backend.singleton.account_manager import AccountManager

class ComplaintFacade:
    def __init__(self):
        self.account_manager = AccountManager()

    def lodge_complaint(self, user_id, complaint_text):
        user = self.account_manager.get_user_by_user_id(user_id)
        if not user:
            return "User not found."
        if 'complaints' not in user:
            user['complaints'] = []
        user['complaints'].append(complaint_text)  # Store as string
        self.account_manager.save_user(user)
        return "Complaint lodged successfully."

    def track_complaints(self, user_id):
        user = self.account_manager.get_user_by_user_id(user_id)
        if not user:
            return "User not found."
        return user.get('complaints', [])