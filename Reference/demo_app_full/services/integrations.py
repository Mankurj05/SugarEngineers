"""
Mock Enterprise Payment Gateway, Audit Ledger, Customer Analytics, and Notification Services.
"""

import datetime
import uuid
from typing import Dict, List, Optional


class PaymentGatewayAdapter:
    """Mock Enterprise Payment Gateway Supporting Stripe, Adyen, and PayPal integrations."""

    def __init__(self, provider: str = "stripe", api_key: str = "sk_test_demo123456"):
        self.provider = provider
        self.api_key = api_key
        self.transaction_log: List[Dict] = []

    def authorize_payment(self, amount: float, currency: str, card_token: str) -> Dict:
        tx_id = f"tx_{uuid.uuid4().hex[:12]}"
        success = amount > 0 and card_token != "tok_declined"
        res = {
            "transaction_id": tx_id,
            "status": "authorized" if success else "declined",
            "amount": amount,
            "currency": currency,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "provider": self.provider,
            "error_code": None if success else "CARD_DECLINED",
        }
        self.transaction_log.append(res)
        return res

    def capture_payment(self, transaction_id: str, amount: float) -> Dict:
        res = {
            "capture_id": f"cap_{uuid.uuid4().hex[:12]}",
            "transaction_id": transaction_id,
            "status": "captured",
            "captured_amount": amount,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
        return res

    def refund_transaction(self, transaction_id: str, amount: float, reason: str = "customer_request") -> Dict:
        res = {
            "refund_id": f"ref_{uuid.uuid4().hex[:12]}",
            "transaction_id": transaction_id,
            "refunded_amount": amount,
            "reason": reason,
            "status": "completed",
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
        return res


class EnterpriseLedgerService:
    """Audit ledger tracking all debits, credits, discounts, taxes, and revenue movements."""

    def __init__(self):
        self.entries: List[Dict] = []

    def record_entry(self, account: str, entry_type: str, amount: float, reference_id: str, metadata: Optional[Dict] = None) -> Dict:
        entry = {
            "entry_id": f"led_{uuid.uuid4().hex[:12]}",
            "account": account,
            "type": entry_type,
            "amount": round(amount, 2),
            "reference_id": reference_id,
            "metadata": metadata or {},
            "recorded_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
        self.entries.append(entry)
        return entry

    def get_account_balance(self, account: str) -> float:
        balance = 0.0
        for entry in self.entries:
            if entry["account"] == account:
                if entry["type"] == "CREDIT":
                    balance += entry["amount"]
                elif entry["type"] == "DEBIT":
                    balance -= entry["amount"]
        return round(balance, 2)


class CustomerAnalyticsEngine:
    """Customer Lifetime Value (LTV), Churn Risk Prediction, and Segment Classifier."""

    def __init__(self):
        self.customer_data: Dict[str, Dict] = {}

    def track_order(self, customer_id: str, order_amount: float) -> Dict:
        if customer_id not in self.customer_data:
            self.customer_data[customer_id] = {
                "order_count": 0,
                "total_spent": 0.0,
                "first_order_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "last_order_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            }

        data = self.customer_data[customer_id]
        data["order_count"] += 1
        data["total_spent"] = round(data["total_spent"] + order_amount, 2)
        data["last_order_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

        # Calculate VIP Tier
        if data["total_spent"] >= 1000.0 or data["order_count"] >= 10:
            tier = "VIP_GOLD"
        elif data["total_spent"] >= 500.0 or data["order_count"] >= 5:
            tier = "VIP_SILVER"
        else:
            tier = "STANDARD"

        data["tier"] = tier
        return data


class NotificationDispatchService:
    """Email, SMS, and Webhook dispatch service for e-commerce transactional events."""

    def __init__(self):
        self.sent_notifications: List[Dict] = []

    def send_order_confirmation(self, email: str, order_id: str, grand_total: float) -> bool:
        notification = {
            "type": "ORDER_CONFIRMATION",
            "recipient": email,
            "order_id": order_id,
            "grand_total": grand_total,
            "status": "DELIVERED",
            "sent_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
        self.sent_notifications.append(notification)
        return True

    def send_shipping_update(self, email: str, order_id: str, tracking_number: str) -> bool:
        notification = {
            "type": "SHIPPING_UPDATE",
            "recipient": email,
            "order_id": order_id,
            "tracking_number": tracking_number,
            "status": "DELIVERED",
            "sent_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
        self.sent_notifications.append(notification)
        return True
