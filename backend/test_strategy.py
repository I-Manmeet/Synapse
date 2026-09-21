from agents.analytics import analyze as analytics
from agents.finance_agent import analyze as finance
from agents.market_agent import analyze as market
from agents.customer_agent import analyze as customer
from agents.risk_agent import assess
from agents.strategy_agent import recommend


question = """
My clothing business sales decreased by 20%
over the last three months.
Identify the major business risks and
recommend a strategy to improve performance.
"""


# Step 1: Run specialist agents
findings = {
    "analytics": analytics(question),
    "finance": finance(question),
    "market": market(question),
    "customer": customer(question)
}


# Step 2: Run Risk Agent
risk = assess(question, findings)

findings["risk"] = risk


# Step 3: Run Strategy Agent
strategy = recommend(question, findings)


print("\n===== STRATEGY AGENT =====\n")
print(strategy)