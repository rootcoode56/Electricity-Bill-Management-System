# backend/facade/billing_facade.py

from backend.singleton.account_manager import AccountManager
from backend.strategy.payment_strategy import PaymentContext, CreditCardPayment, MobilePayment
from backend.observer.observer import NotificationCenter, UserObserver

class BillingFacade:
    def __init__(self):
        self.account_manager = AccountManager()
        self.notification_center = NotificationCenter()
        self.payment_context = None

    def view_bill(self, user_id, month):
        user = self.account_manager.get_user_by_user_id(user_id)
        if not user or 'bills' not in user:
            return "❌ User not found or no billing data."
        
        # Normalize month case
        month = month.capitalize()

        for bill in user['bills']:
            if bill['month'] == month:
                return f"📄 {month} Bill: {bill['amount']} BDT | Paid: {'✅' if bill['paid'] else '❌'}"
        return f"🔍 No bill found for {month}."

    def pay_bill(self, user_id, month, method='card'):
        user = self.account_manager.get_user_by_user_id(user_id)
        if not user or 'bills' not in user:
            return "❌ User not found or no billing data."

        # Normalize month case
        month = month.capitalize()

        # Attach user to observer
        observer = UserObserver(user)
        self.notification_center.attach(observer)

        # Set payment strategy
        if method == 'card':
            self.payment_context = PaymentContext(CreditCardPayment())
        elif method == 'bkash':
            self.payment_context = PaymentContext(MobilePayment())
        else:
            return "❌ Invalid payment method"

        result = self.payment_context.execute_payment(user_id, month)
        self.notification_center.notify(f"💸 Payment processed for {month}: {result}")
        return result
