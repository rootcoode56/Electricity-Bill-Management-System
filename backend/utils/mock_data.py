users = {
    "U001": {
        "user_id": "U001",
        "username": "admin",
        "password": "admin123",
        "name": "Alvi Rahman",
        "address": "Dhaka, Bangladesh",
        "role": "admin",
        "meter_id": None,
        "bills": [],
        "notifications": [],
        "complaints": [],
        "services": []
    },
    "U002": {
        "user_id": "U002",
        "username": "user1",
        "password": "pass1",
        "name": "Alvi Rahman",
        "address": "Dhaka, Bangladesh",
        "role": "customer",
        "meter_id": "M123",
        "bills": [
            {"month": "Jan", "amount": 1000, "paid": True},
            {"month": "Feb", "amount": 1200, "paid": False},
            {"month": "Mar", "amount": 950, "paid": False}
        ],
        "notifications": [],
        "complaints": [],
        "services": []
    },
    "U003": {
        "user_id": "U003",
        "username": "user2",
        "password": "pass2",
        "name": "Rafiul Hasan",
        "address": "Chittagong, Bangladesh",
        "role": "customer",
        "meter_id": "M124",
        "bills": [
            {"month": "Jan", "amount": 1300, "paid": True},
            {"month": "Feb", "amount": 1100, "paid": True}
        ],
        "notifications": [],
        "complaints": [],
        "services": []
    }
}

complaints = []
service_requests = []

def get_mock_data():
    return users