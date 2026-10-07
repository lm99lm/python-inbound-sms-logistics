import os

from src.infrai_client import SmsClient
from shipment_service import InboundSms, ShipmentEvent, acknowledge


def main() -> None:
    recipient = os.environ.get("DEMO_SMS_TO")
    if not recipient:
        raise SystemExit("DEMO_SMS_TO is required")
    result = acknowledge(
        InboundSms(recipient, "Delivered at receiving bay", "2026-09-04T09:00:00Z"),
        ShipmentEvent("SHP-DEMO", "delivered", "2026-09-04T08:55:00Z"),
        SmsClient.from_environment(),
    )
    print(result)


if __name__ == "__main__":
    main()
