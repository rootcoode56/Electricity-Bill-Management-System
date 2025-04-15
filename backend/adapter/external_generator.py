# external_generator.py

class ExternalBillGenerator:
    def generate_monthly_bill(self, user_id, month):
        """
        Simulates generating a bill from an external system.
        """
        # Simulated bill data from an external system
        bill_data = {
            "user_id": user_id,
            "month": month,
            "bill_amount": 120.50,  # Simulated bill amount
            "due_date": f"{month}-15-2025"
        }
        return bill_data
