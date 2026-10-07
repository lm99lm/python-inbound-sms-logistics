from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from src.infrai_client import SmsClient


@dataclass(frozen=True)
class ProofOfDelivery:
    name: str
    content_type: str
    download_url: str


@dataclass(frozen=True)
class ShipmentEvent:
    shipment_id: str
    event: str
    occurred_at: str
    pod_files: list[ProofOfDelivery] = field(default_factory=list)


@dataclass(frozen=True)
class InboundSms:
    from_number: str
    text: str
    received_at: str


def handle_inbound_sms(message: InboundSms, shipment: ShipmentEvent) -> dict[str, Any]:
    normalized = message.text.strip().upper()
    exception = normalized.startswith("EXCEPTION") or normalized.startswith("DAMAGED")
    if exception:
        return {"shipment_id": shipment.shipment_id, "state": "exception", "reason": message.text.strip()}
    return {"shipment_id": shipment.shipment_id, "state": "acknowledged", "event": shipment.event}


def acknowledge(message: InboundSms, shipment: ShipmentEvent, client: SmsClient) -> dict[str, Any]:
    decision = handle_inbound_sms(message, shipment)
    if decision["state"] == "exception":
        client.send(message.from_number, f"Shipment {shipment.shipment_id}: exception recorded.", shipment.shipment_id)
    else:
        client.send(message.from_number, f"Shipment {shipment.shipment_id}: update received.", shipment.shipment_id)
    return decision
