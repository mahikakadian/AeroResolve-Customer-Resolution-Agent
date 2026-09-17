# AeroResolve — Customer-Facing Resolution Agent

A policy-grounded airline disruption resolution agent built for Assignment 3.

## Why this prototype stands out
1. **Policy authority is deterministic.** The agent does not let an LLM invent compensation.
2. **Hard escalation gates.** Legal/formal complaints, prohibited exceptions, and fare-difference waivers above ₹1,500 are routed to a human.
3. **Source trace.** Each result exposes the source categories used.
4. **Customer-safe language.** Empathy is generated without changing the underlying entitlement.
5. **Scenario-ready.** All three assignment scenarios are preloaded for demo.
6. **No fabricated flight inventory.** The data pack does not list actual alternative flight numbers, so the prototype never invents them.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open the local Streamlit URL shown in the terminal.

## Demo scenarios

### 1 — Priya Nair
Cancellation + full refund + business-class upgrade request.
Expected behavior: refund can be initiated to the original payment method; free rebooking can be offered; business-class upgrade request is not supported by the supplied rules and should trigger human review.

### 2 — Arvind Kulkarni
4-hour delay + hotel request.
Expected behavior: meal voucher + lounge access; hotel request should not be granted because the supplied hotel rule starts above 5 hours.

### 3 — Meher Kaur
6-hour delay + full-night hotel + ₹2,000 higher-fare rebooking.
Expected behavior: meal voucher + hotel covering delayed hours only; full-night stay is outside policy; ₹2,000 fare-difference waiver requires supervisor approval.

## Architecture

Customer message → Identity/entity extraction → Disruption classifier → Policy engine → Guardrail gate → Resolution or human escalation → Audit/source trace.

See `architecture.md`.

## Source boundary

The supplied assignment data pack is the only source of customer facts and service rules. The sample prior conversations are treated as tone examples only, not as facts or policy.

## Suggested GitHub structure

- `app.py` — Streamlit UI
- `policy_engine.py` — deterministic decision/guardrail engine
- `data.json` — source-grounded assignment data
- `test_policy.py` — scenario acceptance tests
- `architecture.md` — architecture and process flow
- `demo_script.md` — demo narration
- `requirements.txt` — dependencies
