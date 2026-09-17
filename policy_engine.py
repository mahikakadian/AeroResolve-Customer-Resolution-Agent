
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Optional
import json, re
from pathlib import Path

DATA = json.loads((Path(__file__).parent / "data.json").read_text(encoding="utf-8"))

CUSTOMERS = {c["name"].lower(): c for c in DATA["customers"]}
BOOKINGS = DATA["bookings"]

def lookup_customer(text: str) -> Optional[dict]:
    t = text.lower()
    for name, c in CUSTOMERS.items():
        if name in t or c["pnr"].lower() in t:
            return c
    return None

def booking_for_customer(cust: dict) -> Optional[dict]:
    # Return disrupted booking first.
    candidates = [b for b in BOOKINGS if b["customer"] == cust["name"]]
    disrupted = [b for b in candidates if b["status"].lower() != "unaffected"]
    return disrupted[0] if disrupted else (candidates[0] if candidates else None)

def detect_intent(text: str) -> str:
    t = text.lower()
    if any(x in t for x in ["legal", "lawsuit", "lawyer", "formal complaint", "file a complaint"]):
        return "legal_or_formal_complaint"
    if "refund" in t:
        return "refund"
    if any(x in t for x in ["business class", "upgrade", "upgrade me"]):
        return "upgrade"
    if "hotel" in t:
        return "hotel"
    if any(x in t for x in ["rebook", "rebooking", "different flight", "another flight"]):
        return "rebooking"
    if any(x in t for x in ["compensation", "voucher", "lounge"]):
        return "compensation"
    if any(x in t for x in ["status", "flight", "booking", "cancelled", "canceled", "delayed"]):
        return "status"
    return "general"

def extract_fare_difference(text: str) -> Optional[int]:
    m = re.search(r"(?:₹|rs\.?\s*|inr\s*)?(\d[\d,]*)\s*(?:fare difference|difference)", text.lower())
    if not m:
        m = re.search(r"(?:fare difference|difference)[^\d₹]{0,15}(?:₹|rs\.?\s*|inr\s*)?(\d[\d,]*)", text.lower())
    if m:
        return int(m.group(1).replace(",", ""))
    return None

def resolve(text: str) -> Dict[str, Any]:
    cust = lookup_customer(text)
    if not cust:
        return {
            "status": "needs_identity",
            "intent": detect_intent(text),
            "message": "Please provide your name or booking reference so I can access your booking information.",
            "actions": [],
            "escalate": False,
            "sources": ["Customer Profiles", "Booking / Transaction Data"]
        }

    booking = booking_for_customer(cust)
    intent = detect_intent(text)
    t = text.lower()
    actions = []
    escalation_reasons = []
    facts = []

    if booking:
        facts.append(f"{booking['flight']} | {booking['route']} | {booking['status']}")

    # Hard safety/escalation gates first.
    if intent == "legal_or_formal_complaint":
        escalation_reasons.append("Threat of legal action or formal complaint requires human escalation.")
    if "different payment" in t or "another payment" in t:
        escalation_reasons.append("Refunds cannot be processed to a different payment method.")

    # Determine disruption policy from booking data.
    if booking and booking["status"].lower().startswith("cancelled"):
        if intent in {"refund", "status", "general"} or "cash refund" in t:
            actions.append("Initiate full refund request to the original payment method.")
            facts.append("Refund is processed in full within 7 business days.")
        if intent in {"rebooking", "upgrade"} or "business class" in t:
            # Upgrade request is not a standard entitlement.
            if intent == "upgrade" or "business class" in t:
                escalation_reasons.append("A free business-class upgrade is not provided by the stated loyalty or cancellation rules.")
            actions.append("Offer free rebooking on the next available flight within 24 hours.")
        if "furious" in t:
            facts.append("Customer tone indicates frustration; acknowledge it without changing policy.")

    elif booking and booking["status"].lower().startswith("delayed"):
        hours = int(re.search(r"(\d+)h", booking["status"]).group(1))
        if hours > 5:
            actions.extend([
                "Issue meal voucher.",
                "Arrange hotel accommodation covering the delayed hours only."
            ])
            if intent == "hotel" and ("full night" in t or "whole night" in t):
                escalation_reasons.append("Policy covers only delayed hours, not a full night's stay.")
        elif hours > 3:
            actions.extend([
                "Issue meal voucher.",
                "Provide lounge access."
            ])
            if intent == "hotel":
                escalation_reasons.append("A 4-hour delay qualifies for meal voucher + lounge access, not hotel accommodation.")
        else:
            actions.append("Issue ₹500 meal voucher.")

        if intent in {"rebooking", "upgrade"}:
            diff = extract_fare_difference(text)
            if diff is not None and diff > 1500:
                escalation_reasons.append(f"Fare difference of ₹{diff:,} exceeds ₹1,500; supervisor approval is required to waive it.")
            else:
                actions.append("Higher-fare voluntary rebooking requires payment of the fare difference.")

    # Loyalty fact: priority only, no extra compensation.
    if cust["tier"] in {"Gold", "Platinum"}:
        facts.append(f"{cust['tier']} tier receives priority rebooking, with no additional compensation beyond standard policy.")

    if escalation_reasons:
        response = (
            "I’m sorry this disruption has been frustrating. I can apply the standard policy where permitted, "
            "but the following request needs human review: " + " ".join(escalation_reasons)
        )
        return {
            "status": "escalate",
            "customer": cust["name"],
            "pnr": cust["pnr"],
            "intent": intent,
            "message": response,
            "actions": actions,
            "escalate": True,
            "escalation_reasons": escalation_reasons,
            "facts": facts,
            "sources": ["Customer Profiles", "Booking / Transaction Data", "Service Rules", "Allowed vs. Prohibited Actions"]
        }

    if not actions:
        actions = ["Provide the customer's own booking and flight status information."]

    return {
        "status": "resolved",
        "customer": cust["name"],
        "pnr": cust["pnr"],
        "intent": intent,
        "message": "I’ve checked your booking. " + " ".join(actions),
        "actions": actions,
        "escalate": False,
        "facts": facts,
        "sources": ["Customer Profiles", "Booking / Transaction Data", "Service Rules", "Allowed vs. Prohibited Actions"]
    }
