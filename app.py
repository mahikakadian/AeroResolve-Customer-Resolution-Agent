
import streamlit as st
from policy_engine import resolve, DATA

st.set_page_config(page_title="AeroResolve • Customer Resolution Agent", page_icon="✈️", layout="wide")

st.markdown("""
<style>
.hero {padding: 18px 22px; border-radius: 16px; border: 1px solid #d9dee8; margin-bottom: 18px;}
.small {font-size: 0.88rem; opacity: 0.75;}
</style>
""", unsafe_allow_html=True)

st.title("✈️ AeroResolve")
st.caption("Policy-grounded Customer Resolution Agent • Assignment 3")
st.markdown('<div class="hero"><b>Design principle:</b> the agent separates customer empathy from policy authority. It can resolve permitted actions, but hard escalation gates prevent it from inventing compensation or bypassing rules.</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Try a scenario")
    examples = {
        "Priya • cancellation + refund + upgrade":
            'Priya Nair, SK4821X: My flight was cancelled. I want a full cash refund and a free upgrade to business class on my return flight for the trouble. I am furious.',
        "Arvind • 4h delay + hotel":
            'Arvind Kulkarni, TR1190B: My flight is delayed 4 hours and I missed a meeting. Give me a hotel because this is a long delay.',
        "Meher • 6h delay + full-night hotel + ₹2,000 fare diff":
            'Meher Kaur, WL7742: My flight is delayed 6 hours. I want a full night hotel stay and I want a different higher-fare flight. The fare difference is ₹2,000.',
        "Formal complaint escalation":
            'Priya Nair, SK4821X: I will file a formal complaint and take legal action.'
    }
    selected = st.selectbox("Scenario", list(examples))
    if st.button("Load scenario", use_container_width=True):
        st.session_state["prompt"] = examples[selected]

    st.divider()
    st.subheader("Source boundary")
    st.write("Only the supplied assignment data pack is used as the policy source.")
    st.write("No invented flight numbers, prices, compensation, or customer facts.")

prompt = st.text_area("Customer message", value=st.session_state.get("prompt", ""), height=150,
                      placeholder="Example: Priya Nair, SK4821X: My flight was cancelled...")

if st.button("Resolve request", type="primary", use_container_width=True):
    result = resolve(prompt)
    st.session_state["last_result"] = result

result = st.session_state.get("last_result")
if result:
    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("Decision", "ESCALATE" if result["escalate"] else "RESOLVE")
    c2.metric("Intent", result["intent"].replace("_", " ").title())
    c3.metric("Customer", result.get("customer", "Needs identity"))

    st.subheader("Customer-facing response")
    st.info(result["message"])

    if result.get("actions"):
        st.subheader("Allowed actions / next steps")
        for a in result["actions"]:
            st.write("• " + a)

    if result.get("facts"):
        st.subheader("Grounding facts used")
        for f in result["facts"]:
            st.write("• " + f)

    if result.get("escalation_reasons"):
        st.error("Human escalation required")
        for r in result["escalation_reasons"]:
            st.write("• " + r)

    with st.expander("🔎 Audit trail / source trace"):
        st.write("Sources consulted:")
        for s in result.get("sources", []):
            st.write("• " + s)
        st.caption("Prototype intentionally exposes the reasoning trace at a high level without revealing hidden chain-of-thought.")

st.divider()
st.subheader("Agent capability map")
cols = st.columns(4)
cards = [
    ("Identity", "Recognizes customer/PNR from the supplied profiles."),
    ("Policy engine", "Applies explicit cancellation, delay, refund, fare and loyalty rules."),
    ("Guardrails", "Escalates prohibited exceptions before taking action."),
    ("Auditability", "Shows customer-facing decision + source categories used.")
]
for col, (h, b) in zip(cols, cards):
    with col:
        st.markdown(f"**{h}**")
        st.write(b)
