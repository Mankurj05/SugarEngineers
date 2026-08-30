"""
Multi-Tenant Domain Manager, API Rate Limiter, and Webhook Event Dispatcher.
"""

import datetime
import uuid
from typing import Dict, List, Optional


class MultiTenantContextManager:
    """Enterprise Multi-Tenancy Tenant Isolation & Domain Scoping."""

    def __init__(self):
        self.tenants: Dict[str, Dict] = {
            "tenant_default": {"name": "Default Retailer", "tier": "ENTERPRISE", "status": "ACTIVE"},
            "tenant_acme": {"name": "Acme Corp Store", "tier": "PRO", "status": "ACTIVE"},
            "tenant_globex": {"name": "Globex Retail", "tier": "ENTERPRISE", "status": "ACTIVE"},
        }

    def validate_tenant(self, tenant_id: str) -> bool:
        tenant = self.tenants.get(tenant_id)
        return tenant is not None and tenant["status"] == "ACTIVE"


class APIRateLimiterThrottler:
    """Sliding Window Rate Limiter for E-Commerce Public API Protection."""

    def __init__(self, requests_per_minute: int = 100):
        self.limit = requests_per_minute
        self.request_history: Dict[str, List[float]] = {}

    def is_rate_limited(self, client_ip: str, timestamp: float) -> bool:
        if client_ip not in self.request_history:
            self.request_history[client_ip] = []

        # Remove requests older than 60 seconds
        window_start = timestamp - 60.0
        self.request_history[client_ip] = [
            t for t in self.request_history[client_ip] if t > window_start
        ]

        if len(self.request_history[client_ip]) >= self.limit:
            return True

        self.request_history[client_ip].append(timestamp)
        return False


class WebhookEventDispatcher:
    """Transactional Event Publisher for Third-Party Webhook Consumers."""

    def __init__(self):
        self.registered_webhooks: Dict[str, List[str]] = {
            "order.created": ["https://analytics.partner.com/webhook", "https://erp.internal.com/events"],
            "order.paid": ["https://fulfillment.3pl.com/api/webhooks"],
            "cart.abandoned": ["https://email-marketing.io/hooks"]
        }
        self.dispatch_log: List[Dict] = []

    def trigger_event(self, event_type: str, payload: Dict) -> int:
        urls = self.registered_webhooks.get(event_type, [])
        dispatched_count = 0
        for url in urls:
            log_entry = {
                "event_id": f"evt_{uuid.uuid4().hex[:10]}",
                "event_type": event_type,
                "target_url": url,
                "payload": payload,
                "status": "DISPATCHED",
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }
            self.dispatch_log.append(log_entry)
            dispatched_count += 1
        return dispatched_count
