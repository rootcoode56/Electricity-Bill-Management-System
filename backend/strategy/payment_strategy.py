# backend/strategy/payment_strategy.py

from abc import ABC, abstractmethod
from backend.singleton.account_manager import AccountManager

# --- Strategy Interface ---
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, user_id, month):
        pass

# --- Concrete Strategy 1: Credit Card ---
class CreditCardPayment(PaymentStrategy):
    def pay(self, user_id, month):
        user = AccountManager().get_user_by_user_id(user_id)
        for bill in user["bills"]:
            if bill["month"] == month and not bill["paid"]:
                bill["paid"] = True
                return f"Paid {bill['amount']} via Credit Card for {month}."
        return "No due found for the selected month."

# --- Concrete Strategy 2: Mobile Payment (e.g., Bkash) ---
class MobilePayment(PaymentStrategy):
    def pay(self, user_id, month):
        user = AccountManager().get_user_by_user_id(user_id)
        for bill in user["bills"]:
            if bill["month"] == month and not bill["paid"]:
                bill["paid"] = True
                return f"Paid {bill['amount']} via Mobile Payment (Bkash) for {month}."
        return "No due found for the selected month."

# --- Context Class ---
class PaymentContext:
    def __init__(self, strategy: PaymentStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: PaymentStrategy):
        self._strategy = strategy

    def execute_payment(self, user_id, month):
        return self._strategy.pay(user_id, month)
