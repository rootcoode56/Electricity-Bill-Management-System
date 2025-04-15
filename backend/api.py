import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, jsonify, request, send_from_directory
from backend.singleton.account_manager import AccountManager
from backend.facade.billing_facade import BillingFacade
from backend.facade.complaint_facade import ComplaintFacade
from backend.factory.service_factory import ServiceApplicationHandler
from backend.strategy.search_strategy import UserSearchContext, SearchByMeterID, SearchByUserID

app = Flask(__name__, static_folder="../frontend", template_folder="../frontend")

account_manager = AccountManager()
billing_facade = BillingFacade()
complaint_facade = ComplaintFacade()
service_handler = ServiceApplicationHandler()

# Serve frontend files
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return jsonify({'error': 'File not found'}), 404

# Login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password required'}), 400
    user_id = account_manager.authenticate(username, password)
    if user_id:
        user = account_manager.get_user_by_user_id(user_id)
        return jsonify({
            'success': True,
            'user_id': user_id,
            'role': user.get('role', 'customer')
        })
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

# Customer: View bill
@app.route('/api/bills/<user_id>', methods=['GET'])
def view_bill(user_id):
    month = request.args.get('month')
    if not month:
        return jsonify({'error': 'Month required'}), 400
    user = account_manager.get_user_by_user_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    try:
        result = billing_facade.view_bill(user_id, month)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Customer: Pay bill
@app.route('/api/bills/<user_id>/pay', methods=['POST'])
def pay_bill(user_id):
    data = request.json or {}
    month = data.get('month')
    payment_method = data.get('payment_method')
    if not month or not payment_method:
        return jsonify({'error': 'Month and payment method required'}), 400
    user = account_manager.get_user_by_user_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    try:
        result = billing_facade.pay_bill(user_id, month, payment_method)
        if "successfully" in result.lower():
            account_manager.notify_user(user_id, f"Bill for {month} paid successfully via {payment_method}")
        return jsonify({'message': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Customer: Lodge complaint
@app.route('/api/complaints/<user_id>', methods=['POST'])
def lodge_complaint(user_id):
    data = request.json or {}
    complaint_text = data.get('complaint_text')
    if not complaint_text:
        return jsonify({'error': 'Complaint text required'}), 400
    user = account_manager.get_user_by_user_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    try:
        result = complaint_facade.lodge_complaint(user_id, complaint_text)
        if "successfully" in result.lower():
            account_manager.notify_user(user_id, "Your complaint has been lodged successfully")
        return jsonify({'message': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Customer: Track complaints
@app.route('/api/complaints/<user_id>', methods=['GET'])
def track_complaints(user_id):
    user = account_manager.get_user_by_user_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    try:
        result = complaint_facade.track_complaints(user_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Customer: Apply for service
@app.route('/api/services/<user_id>', methods=['POST'])
def apply_service(user_id):
    data = request.json or {}
    service_type = data.get('service_type')
    connection_data = data.get('connection_data')
    if not service_type:
        return jsonify({'error': 'Service type required'}), 400
    user = account_manager.get_user_by_user_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    try:
        result = service_handler.apply_for_service(user_id, service_type, connection_data)
        if "successfully" in result.lower():
            if service_type == "new_connection":
                account_manager.notify_user(user_id, "New connection request submitted successfully")
            elif service_type == "meter_change":
                account_manager.notify_user(user_id, "Meter change request submitted successfully")
            elif service_type == "name_correction":
                account_manager.notify_user(user_id, "Name correction request submitted successfully")
        return jsonify({'message': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Customer: View notifications
@app.route('/api/notifications/<user_id>', methods=['GET'])
def get_notifications(user_id):
    user = account_manager.get_user_by_user_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    try:
        notifications = user.get('notifications', [])
        return jsonify(notifications)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin: View all users
@app.route('/api/admin/users', methods=['GET'])
def view_all_users():
    try:
        users = account_manager.users
        return jsonify(users)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin: Manage user requests
@app.route('/api/admin/requests', methods=['GET'])
def manage_requests():
    try:
        users = account_manager.users
        requests = []
        for user_id, user_info in users.items():
            if user_info.get('services'):
                for service in user_info['services']:
                    requests.append({
                        'user_id': user_id,
                        'name': user_info['name'],
                        'service': service
                    })
        return jsonify(requests)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin: View bill details
@app.route('/api/admin/bills', methods=['GET'])
def view_all_bills():
    try:
        users = account_manager.users
        bills = []
        for user_id, user_info in users.items():
            for bill in user_info.get('bills', []):
                bills.append({
                    'user_id': user_id,
                    'name': user_info['name'],
                    'bill': bill
                })
        return jsonify(bills)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin: Track complaints
@app.route('/api/admin/complaints', methods=['GET'])
def track_all_complaints():
    try:
        users = account_manager.users
        complaints = []
        for user_id, user_info in users.items():
            for complaint in user_info.get('complaints', []):
                complaints.append({
                    'user_id': user_id,
                    'name': user_info['name'],
                    'complaint': complaint  # Should be a string
                })
        return jsonify(complaints)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin: Search user
@app.route('/api/admin/search', methods=['GET'])
def search_user():
    search_type = request.args.get('search_type')
    query = request.args.get('query')
    if not search_type or not query:
        return jsonify({'error': 'Search type and query required'}), 400
    if search_type not in ['user_id', 'meter_id']:
        return jsonify({'error': 'Invalid search type'}), 400
    try:
        context = UserSearchContext(SearchByUserID() if search_type == 'user_id' else SearchByMeterID())
        user = context.execute_search(query)
        if user:
            return jsonify(user)
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)