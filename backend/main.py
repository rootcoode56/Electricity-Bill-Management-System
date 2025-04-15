import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.singleton.account_manager import AccountManager
from backend.facade.billing_facade import BillingFacade
from backend.facade.complaint_facade import ComplaintFacade
from backend.factory.service_factory import ServiceApplicationHandler
from backend.strategy.search_strategy import UserSearchContext, SearchByMeterID, SearchByUserID

def display_customer_menu():
    print("\nElectricity Bill Management System (Customer)")
    print("1. View Bill")
    print("2. Pay Bill")
    print("3. Lodge a Complaint")
    print("4. Track Complaints")
    print("5. Apply for New Connection")
    print("6. Apply for Meter Change")
    print("7. Apply for Name Correction")
    print("8. View Notifications")
    print("9. Exit")

def display_admin_menu():
    print("\nElectricity Bill Management System (Admin)")
    print("1. View All Users")
    print("2. Manage User Requests")
    print("3. View Bill Details")
    print("4. Track Complaints")
    print("5. Search User")
    print("6. Exit")

def login(account_manager):
    print("Welcome to the system!")
    username = input("Enter username: ")
    password = input("Enter password: ")
    user_id = account_manager.authenticate(username, password)
    if user_id:
        return user_id
    return None

def admin_interface(account_manager):
    print("Admin Login Successful")
    while True:
        display_admin_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            print("Viewing all users...")
            users = account_manager.users
            if users:
                for user_id, user_info in users.items():
                    print(f"User ID: {user_id}, Name: {user_info['name']}, Address: {user_info['address']}, Meter ID: {user_info.get('meter_id', 'N/A')}")
            else:
                print("No users found.")

        elif choice == "2":
            print("Managing user requests...")
            if account_manager.users:
                for user_id, user_info in account_manager.users.items():
                    if user_info["services"]:
                        print(f"User {user_info['name']} has service requests:")
                        for service in user_info["services"]:
                            print(f"- {service}")
            else:
                print("No user service requests found.")

        elif choice == "3":
            print("Viewing bill details...")
            for user_id, user_info in account_manager.users.items():
                print(f"Bill details for {user_info['name']}:")
                for bill in user_info.get('bills', []):
                    print(f"Month: {bill['month']}, Amount: {bill['amount']}, Paid: {bill['paid']}")

        elif choice == "4":
            print("Tracking complaints...")
            for user_id, user_info in account_manager.users.items():
                if user_info.get('complaints'):
                    print(f"Complaints for {user_info['name']}:")
                    for complaint in user_info['complaints']:
                        print(f"- {complaint}")
                else:
                    print(f"No complaints for {user_info['name']}.")

        elif choice == "5":
            search_type = input("Search by (1) User ID or (2) Meter ID? Enter 1 or 2: ")
            query = input("Enter search query: ")
            context = UserSearchContext(SearchByUserID() if search_type == "1" else SearchByMeterID())
            user = context.execute_search(query)
            if user:
                print(f"User found: ID: {user['user_id']}, Name: {user['name']}, Address: {user['address']}, Meter ID: {user.get('meter_id', 'N/A')}")
            else:
                print("❌ User not found.")

        elif choice == "6":
            print("Exiting admin interface... Returning to login.")
            break

        else:
            print("Invalid choice, please try again.")

def customer_interface(user_id, account_manager, billing_facade, complaint_facade, service_handler):
    print(f"Customer Login Successful for user {user_id}")
    while True:
        display_customer_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            month = input("Enter month (e.g., 'Jan'): ")
            print(billing_facade.view_bill(user_id, month))

        elif choice == "2":
            month = input("Enter month (e.g., 'Jan'): ")
            payment_method = input("Enter payment method (card/bkash): ")
            result = billing_facade.pay_bill(user_id, month, payment_method)
            print(result)
            if "successfully" in result.lower():
                account_manager.notify_user(user_id, f"Bill for {month} paid successfully via {payment_method}")

        elif choice == "3":
            complaint_text = input("Enter your complaint: ")
            result = complaint_facade.lodge_complaint(user_id, complaint_text)
            print(result)
            if "successfully" in result.lower():
                account_manager.notify_user(user_id, "Your complaint has been lodged successfully")

        elif choice == "4":
            print(complaint_facade.track_complaints(user_id))

        elif choice == "5":
            print("Applying for New Connection")
            name = input("Enter name: ")
            address = input("Enter address: ")
            connection_data = {"name": name, "address": address}
            result = service_handler.apply_for_service(user_id, "new_connection", connection_data)
            print(result)
            if "successfully" in result.lower():
                account_manager.notify_user(user_id, "New connection request submitted successfully")

        elif choice == "6":
            result = service_handler.apply_for_service(user_id, "meter_change")
            print(result)
            if "successfully" in result.lower():
                account_manager.notify_user(user_id, "Meter change request submitted successfully")

        elif choice == "7":
            result = service_handler.apply_for_service(user_id, "name_correction")
            print(result)
            if "successfully" in result.lower():
                account_manager.notify_user(user_id, "Name correction request submitted successfully")

        elif choice == "8":
            user = account_manager.get_user_by_user_id(user_id)
            notifications = user.get('notifications', [])
            if notifications:
                print("Your Notifications:")
                for i, notification in enumerate(notifications, 1):
                    print(f"{i}. {notification}")
            else:
                print("No notifications found.")

        elif choice == "9":
            print("Exiting customer interface... Returning to login.")
            break

        else:
            print("Invalid choice, please try again.")

def main():
    account_manager = AccountManager()
    billing_facade = BillingFacade()
    complaint_facade = ComplaintFacade()
    service_handler = ServiceApplicationHandler()

    while True:
        user_id = login(account_manager)
        if not user_id:
            print("❌ Invalid credentials! Try again.")
            continue

        user = account_manager.get_user_by_user_id(user_id)
        if user and user["role"] == "admin":
            admin_interface(account_manager)
        else:
            customer_interface(user_id, account_manager, billing_facade, complaint_facade, service_handler)

if __name__ == "__main__":
    main()