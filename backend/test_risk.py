from agents.analytics import analyze as analytics
from agents.finance_agent import analyze as finance
from agents.market_agent import analyze as market
from agents.customer_agent import analyze as customer
from agents.risk_agent import assess


question = """
My clothing business sales decreased by 20%
over the last three months.
Identify the major business risks.
"""


findings = {
    "analytics": analytics(question),
    "finance": finance(question),
    "market": market(question),
    "customer": customer(question)
}


risk = assess(question, findings)


print("\n===== RISK AGENT =====\n")
print(risk)