# 3–4 Minute Demo Script

## Opening — 20 seconds
"Meet AeroResolve, a policy-grounded customer resolution agent for airline disruptions. Its differentiator is simple: the conversational AI can understand the customer, but a deterministic policy layer controls what the agent is actually allowed to do."

## Scenario 1 — Priya — ~60 seconds
Load:
"Priya Nair, SK4821X: My flight was cancelled. I want a full cash refund and a free business-class upgrade on my return flight. I am furious."

Point out:
- Agent identifies Priya and her cancelled SK-204 booking.
- Refund is permitted for an airline-caused cancellation and goes to the original payment method.
- Refund processing is within 7 business days.
- Gold status provides priority rebooking but no extra compensation.
- Business-class upgrade is not stated as an entitlement, so the request is escalated instead of invented.

Say:
"Notice the agent doesn't hallucinate a premium upgrade just to satisfy the customer."

## Scenario 2 — Arvind — ~45 seconds
Load:
"Arvind Kulkarni, TR1190B: My flight is delayed 4 hours. Give me a hotel."

Point out:
- 4-hour delay qualifies for meal voucher + lounge access.
- Hotel is not granted because the hotel rule applies to delays of more than 5 hours.
- The customer can still be acknowledged empathetically.

Say:
"The agent distinguishes frustration from entitlement. It doesn't turn an emotional request into an unsupported benefit."

## Scenario 3 — Meher — ~60 seconds
Load:
"Meher Kaur, WL7742: My flight is delayed 6 hours. I want a full night hotel and a higher-fare flight. Fare difference is ₹2,000."

Point out:
- 6 hours qualifies for meal voucher + hotel for delayed hours only.
- Full-night hotel is outside the stated rule.
- ₹2,000 is above the ₹1,500 waiver threshold, so supervisor approval is required.
- Platinum gets priority rebooking but no additional compensation.

Say:
"This is the strongest guardrail demo: multiple simultaneous requests, multiple policies, one controlled response."

## Closing — 20 seconds
"The architecture is hybrid: natural-language understanding on the front, deterministic policy authority in the middle, and a human escalation path when the agent reaches a prohibited boundary."
