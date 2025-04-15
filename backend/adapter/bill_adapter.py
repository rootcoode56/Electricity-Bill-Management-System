# bill_adapter.py
from adapter.external_generator import ExternalBillGenerator

class BillAdapter:
    def __init__(self):
        self.external_generator = ExternalBillGenerator()

    def get_bill(self, user_id, month):
        """
        Adapts the external bill data to the internal system format.
        """
        external_bill = self.external_generator.generate_monthly_bill(user_id, month)

        # Adapting data format to the system's format
        internal_bill = {
            "user_id": external_bill["user_id"],
            "month": external_bill["month"],
            "amount": external_bill["bill_amount"],
            "due_date": external_bill["due_date"]
        }

        return internal_bill
