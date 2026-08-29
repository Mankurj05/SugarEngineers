# OrderFlow

OrderFlow is a deterministic e-commerce order and pricing management platform built for API regression and dependency-graph analysis. The backend is the primary product: FastAPI routes call domain services, which call explicit pricing rules and in-memory repositories.

## Architecture

`backend/main.py` exposes the FastAPI app. The domain module contains the seeded repositories, Pydantic contracts, services, core rules, and route handlers used by the API. The important path is `route -> service -> pricing/inventory/payment service -> core rule/repository`. `calculate_order_total` is reused by cart quotes, checkout preview, order creation, invoices, and customer summaries.

The baseline pricing rule is correct: conflicting or exclusive coupons cannot be stacked; customer discounts are included in the discount stage; tax is calculated from the post-discount item subtotal; shipping uses the post-discount subtotal and a $200 free-shipping threshold. These are intentionally easy to change in a future demo branch, but no regression is included here.

## Setup

Backend:
```bash
python -m pip install -r backend/requirements.txt
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Frontend uses the existing Next.js dev shell:
```bash
pnpm install
pnpm dev
```

The console calls `http://127.0.0.1:8000/api` and shows the seeded operational data.

## API

- `GET /api/health`
- `GET /api/products?search=&category=` and `GET /api/products/{product_id}`
- `GET /api/customers/{customer_id}` and `/summary`
- `GET /api/inventory/{product_id}`
- `POST /api/cart/quote`
- `POST /api/checkout/preview`
- `POST /api/orders`, `GET /api/orders`, `GET /api/orders/{id}`, `/status`
- `GET /api/invoices/{invoice_id}`
- `POST /api/payments/simulate`
- `POST /api/refunds`
- `GET /api/analytics`

Sample request:
```json
{"customer_id":"CUSTOMER-001","items":[{"product_id":"PROD-001","quantity":1}],"coupon_codes":["WELCOME10"]}
```

Responses are deterministic: fixed IDs, seeded prices and inventory, fixed order timestamps, no external services, random IDs, or runtime timestamps.

## Tests

```bash
pytest tests -q
```

The suite covers catalog, customers, inventory, quotes, checkout, coupon conflicts, order lifecycle, payments, refunds, invoices, summaries, and invalid requests.
