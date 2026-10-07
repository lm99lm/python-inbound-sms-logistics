from shipment_service import InboundSms, ShipmentEvent, handle_inbound_sms


def test_damaged_reply_enters_exception_state():
    result = handle_inbound_sms(
        InboundSms("+15550001", "Damaged pallet at dock 4", "2026-09-04T09:00:00Z"),
        ShipmentEvent("SHP-42", "out_for_delivery", "2026-09-04T08:30:00Z"),
    )
    assert result == {"shipment_id": "SHP-42", "state": "exception", "reason": "Damaged pallet at dock 4"}
