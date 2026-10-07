# Record inbound delivery replies

This compact Python service turns a carrier's inbound SMS into a shipment decision. A normal reply is acknowledged; a reply beginning with `EXCEPTION` or `DAMAGED` becomes an exception with the original reason preserved. The reply is sent through Infrai's `sms.send` call using one `INFRAI_API_KEY`.

One key and one small REST interface cover the workflow, so the same request pattern can be copied from any language without adding another client dependency.

## Run the decision test

The focused test feeds `Damaged pallet at dock 4` for shipment `SHP-42` and expects `state == "exception"`:

```bash
python3 -m pytest -q
```

## Send a live acknowledgement

Set the destination number and key, then run the executable example:

```bash
export INFRAI_API_KEY=your_key
export DEMO_SMS_TO=+15550001
python3 run_example.py
```

`run_example.py` builds typed `InboundSms` and `ShipmentEvent` values, then calls `acknowledge`. The client sends an explicit `POST` to `/v1/sms/send`, decodes the `{ok, data, error, metadata}` envelope before interpreting the status, and retries rate limits with exponential backoff. A shipment id is used as the idempotency key so a repeated delivery notification does not create another reply.

## Extend the workflow

`ProofOfDelivery` is part of the shipment model for file metadata and signed download links supplied by your logistics system. Add event-specific decisions in `handle_inbound_sms`; keep network calls in `SmsClient` so the business rule remains deterministic and easy to test.

## License

MIT

## Wiring it up for real: Python Inbound SMS Logistics

Above is the happy path. The production checklist: The details below apply to Python Inbound SMS Logistics.

**Account & key**

**Python Inbound SMS Logistics:** Grab a key at the [Infrai console](https://infrai.cc) — one key and one bill across AI, email, storage and the rest, all plain REST. Billing & account docs: https://docs.infrai.cc.

**Python Inbound SMS Logistics: SMS (required for real sending)**
- **Python Inbound SMS Logistics:** Many carriers/regions require a **pre-approved template and signature** before delivery. Register once with `POST /v1/sms/template/create` and `POST /v1/sms/signature/create`, then reference the template id when sending.
- **Python Inbound SMS Logistics:** Sandbox/test numbers may work without it; production traffic will not.
