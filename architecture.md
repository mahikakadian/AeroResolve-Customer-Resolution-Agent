# Architecture & Process Flow

## High-level architecture

```text
                         ┌──────────────────────────┐
                         │ Customer message / query │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────┐
                    │ 1. Identity + entity extraction │
                    │ Name / PNR / intent / amount     │
                    └───────────────┬─────────────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────────┐
                    │ 2. Source-grounded lookup       │
                    │ Customer + booking + policy data│
                    └───────────────┬─────────────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────────┐
                    │ 3. Policy decision engine       │
                    │ cancellation / delay / refund / │
                    │ fare / loyalty rules             │
                    └───────────────┬─────────────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────────┐
                    │ 4. HARD GUARDRAIL GATE           │
                    │ prohibited action? legal threat? │
                    │ >₹1,500 waiver?                  │
                    └───────────────┬─────────────────┘
                             ┌──────┴──────┐
                             │             │
                          NO │             │ YES
                             ▼             ▼
                ┌─────────────────┐  ┌──────────────────┐
                │ Safe resolution │  │ Human escalation │
                │ + allowed action│  │ + reason         │
                └────────┬────────┘  └─────────┬────────┘
                         │                     │
                         └──────────┬──────────┘
                                    ▼
                    ┌─────────────────────────────────┐
                    │ Customer response + audit trace │
                    └─────────────────────────────────┘
```

## Design decision

This is a **hybrid agent** rather than a free-form chatbot.

- The conversational layer handles intent and natural-language interaction.
- The policy engine is deterministic and grounded in the supplied data pack.
- Guardrails run before any action is presented as permitted.
- The prototype never fabricates alternative flight inventory, because the source does not provide it.

## Inputs

- Customer name / PNR from the customer message.
- Booking/transaction status.
- Loyalty tier.
- Delay/cancellation facts.
- Explicit customer request.
- Fare difference if supplied by the customer.

## Sources

Only the supplied Assignment 3 data pack:
- Customer Profiles
- Booking / Transaction Data
- Service Rules
- Allowed vs. Prohibited Actions
- Sample conversations only for tone/style

## Assumptions

1. A request is evaluated against the supplied booking associated with the supplied customer/PNR.
2. Where an alternative flight is required by policy, the agent can offer the policy entitlement but does not invent a flight number or schedule.
3. "Free upgrade" is treated as a request for additional benefit beyond the stated standard policy and therefore not auto-approved.
4. A fare-difference waiver above ₹1,500 requires supervisor approval.
5. Formal complaint/legal-action language is escalated immediately.

## AI tools used / how used

For the submission, describe the implementation as:
- **Generative AI / LLM layer (optional production layer):** classify intent, extract entities, and phrase empathetic customer-facing responses.
- **Deterministic policy engine:** validates every proposed action against the supplied rules.
- **Streamlit:** clickable prototype/UI.
- **GitHub:** version control and reproducible submission.
- **Google Drive:** demo video hosting with public access.

The key distinction is that the LLM is not the authority for compensation. Policy decisions are validated by the rules engine.

## Production evolution

A production version could replace the local JSON source with a governed knowledge base and add tool adapters for booking/rebooking/refund systems. Those integrations are intentionally not simulated in this assignment because the data pack does not provide live airline inventory or transaction APIs.
