
from policy_engine import resolve

cases = [
    (
        "Priya refund + upgrade",
        'Priya Nair SK4821X: My flight was cancelled. I want a full cash refund and a free upgrade to business class on my return flight.',
        True,
        ["Initiate full refund request to the original payment method."]
    ),
    (
        "Arvind 4h hotel",
        'Arvind Kulkarni TR1190B: My flight is delayed 4 hours. Give me a hotel.',
        True,
        ["Issue meal voucher.", "Provide lounge access."]
    ),
    (
        "Meher 6h full night + 2000",
        'Meher Kaur WL7742: My flight is delayed 6 hours. I want a full night hotel stay and a different higher-fare flight. Fare difference is ₹2,000.',
        True,
        ["Issue meal voucher.", "Arrange hotel accommodation covering the delayed hours only."]
    ),
    (
        "Priya refund only",
        'Priya Nair SK4821X: Please process my refund.',
        False,
        ["Initiate full refund request to the original payment method."]
    ),
]

for name, text, should_escalate, expected_actions in cases:
    r = resolve(text)
    assert r["escalate"] == should_escalate, (name, r)
    for a in expected_actions:
        assert a in r["actions"], (name, r)

print("All acceptance tests passed.")
