"""
Synapse — Multi-Agent Business Intelligence (polished + visuals)
Run:  streamlit run app.py

WHO OWNS WHAT (see the INTEGRATION GUIDE comment below):
  Analytics, Finance  -> JIYA        Market, Customer -> ANUPAM
  Risk, Strategy      -> MANMEET (done)
"""
import os
import json
import time

import streamlit as st
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

# ============================================================================
# Model connection
# ============================================================================
def _base_endpoint() -> str:
    ep = os.getenv("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
    if ep.endswith("/openai/v1"):
        ep = ep[: -len("/openai/v1")]
    return ep + "/"


client = AzureOpenAI(
    azure_endpoint=_base_endpoint(),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview"),
)
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4.1-mini")


def ask(system_prompt: str, user_content: str, temperature: float = 0.3) -> str:
    resp = client.chat.completions.create(
        model=DEPLOYMENT,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        temperature=temperature,
    )
    return resp.choices[0].message.content or ""


# ===========================================================================
# INTEGRATION GUIDE — WHO CHANGES WHAT
# ---------------------------------------------------------------------------
# The 4 specialist agents below are TEMPORARY placeholder prompts so this demo
# runs on its own. Each teammate replaces THEIR placeholder with their real
# agent. Risk + Strategy (further down) are Manmeet's real agents — done.
#
#   Analytics  ->  JIYA     (real version: reads sales data, exact math)
#   Finance    ->  JIYA     (real version: margins, ROI, cash flow)
#   Market     ->  ANUPAM   (real version: web search / competitor data)
#   Customer   ->  ANUPAM   (real version: sentiment over real reviews)
#   Risk       ->  MANMEET  (DONE — real prompt below)
#   Strategy   ->  MANMEET  (DONE — real prompt below)
#
# HOW TO PLUG IN A REAL AGENT (2 options):
#   (A) Just improve the prompt string here, OR
#   (B) Import your real agent function and call it in the run loop instead of
#       `ask(...)`. Your agent only needs to take the question and return text:
#           from agents.analytics import analyze
#           findings["Analytics"] = analyze(question)
#   Keep the return type a string so Risk + Strategy keep working unchanged.
# ===========================================================================
SPECIALISTS = {
    # >>> JIYA: replace these two stubs with your real Analytics + Finance agents
    "Analytics": "You are a business Analytics agent. Analyze sales, performance, trends and KPIs for the question. State assumptions if data is missing. 3-4 short bullets.",   # JIYA
    "Finance": "You are a Finance agent. Analyze revenue, costs, margins, ROI and feasibility. State assumptions if data is missing. 3-4 short bullets.",   # JIYA
    # >>> ANUPAM: replace these two stubs with your real Market + Customer agents
    "Market": "You are a Market Research agent. Analyze competitors, pricing and market trends. State assumptions if data is missing. 3-4 short bullets.",   # ANUPAM
    "Customer": "You are a Customer Intelligence agent. Analyze sentiment, complaints and behavior. State assumptions if data is missing. 3-4 short bullets.",   # ANUPAM
}

# >>> MANMEET (DONE): real Risk agent
RISK_PROMPT = (
    "You are the Risk Assessment agent. Rate the risk in each relevant category using "
    "LOW / MEDIUM / HIGH with a one-line reason grounded in a finding, then list 2-3 "
    "mitigations. Write 'insufficient data' where there is none. Never invent data."
)
# >>> MANMEET (DONE): real Strategy agent
STRATEGY_PROMPT = (
    "You are the Strategy agent — the final decision-support step. Synthesize the "
    "findings into ONE recommendation. Format exactly:\n"
    "Bottom line: <two sentences>\n"
    "Recommended actions:\n1. ...\n2. ...\n3. (optional)\n"
    "Biggest caveat: <one line>\n"
    "Interpret the findings, don't repeat them. Be decisive but honest. Never invent data."
)
RISK_JSON_PROMPT = (
    "Based ONLY on the findings, output a compact JSON object rating these risk "
    "categories as LOW, MEDIUM, or HIGH: Financial, Market, Operational, Customer, "
    'Competition. Example: {"Financial":"HIGH","Market":"MEDIUM","Operational":"LOW",'
    '"Customer":"LOW","Competition":"MEDIUM"}. Output JSON only, no other text.'
)

AGENT_META = {
    "Analytics": ("Data Analyst", "📊"), "Finance": ("CFO", "💰"),
    "Market": ("Market Research", "🔍"), "Customer": ("Customer Intelligence", "👥"),
    "Risk": ("Risk Manager", "⚠️"), "Strategy": ("Decision Support", "🎯"),
}
LEVELS = {"LOW": (1, "#10b981"), "MEDIUM": (2, "#f59e0b"), "HIGH": (3, "#ef4444")}


def _format(findings: dict) -> str:
    return "\n".join(f"- {name}: {text}" for name, text in findings.items())


def risk_scores(findings: dict) -> dict:
    """Ask the model for machine-readable risk levels; safe fallback to {}."""
    raw = ask(RISK_JSON_PROMPT, f"Findings:\n{_format(findings)}", temperature=0)
    try:
        return json.loads(raw[raw.index("{"): raw.rindex("}") + 1])
    except Exception:
        return {}


# ============================================================================
# Styling
# ============================================================================
st.set_page_config(page_title="Synapse BI", page_icon="🧠", layout="wide")
st.markdown("""
<style>
#MainMenu, header, footer {visibility: hidden;}
.block-container {padding-top: 2rem; max-width: 1120px;}
.hero {background: linear-gradient(120deg,#4f46e5 0%,#7c3aed 100%); border-radius:18px;
  padding:34px 40px; margin-bottom:26px; color:#fff; box-shadow:0 10px 30px rgba(79,70,229,.25);}
.hero h1 {font-size:34px; margin:0 0 6px; font-weight:700; letter-spacing:-.5px;}
.hero p {margin:0; opacity:.92; font-size:15px;}
.hero .badge {display:inline-block; background:rgba(255,255,255,.18); padding:4px 12px;
  border-radius:20px; font-size:12px; margin-bottom:14px; letter-spacing:.4px;}
.agents {display:grid; grid-template-columns:repeat(6,1fr); gap:12px; margin:8px 0 4px;}
.agent {background:#fff; border:1px solid #ececf3; border-radius:14px; padding:16px 12px;
  text-align:center; transition:all .25s ease;}
.agent .emoji{font-size:24px;} .agent .name{font-weight:700;font-size:14px;color:#1e1b39;margin-top:6px;}
.agent .role{font-size:11px;color:#8b8aa0;margin-top:2px;}
.agent .dot{width:9px;height:9px;border-radius:50%;margin:10px auto 0;background:#d7d7e2;}
.agent.running{border-color:#f59e0b;box-shadow:0 6px 18px rgba(245,158,11,.18);}
.agent.running .dot{background:#f59e0b;animation:pulse 1s infinite;}
.agent.done{border-color:#10b981;box-shadow:0 6px 18px rgba(16,185,129,.15);}
.agent.done .dot{background:#10b981;}
@keyframes pulse{0%{opacity:1;}50%{opacity:.35;}100%{opacity:1;}}
.metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:8px 0;}
.metric{background:#fff;border:1px solid #ececf3;border-radius:14px;padding:18px 20px;
  box-shadow:0 6px 18px rgba(30,27,57,.05);}
.metric .v{font-size:24px;font-weight:700;color:#1e1b39;} .metric .l{font-size:12px;color:#8b8aa0;letter-spacing:.4px;}
.rk{display:flex;align-items:center;gap:12px;margin:8px 0;}
.rk-label{width:110px;font-size:13px;color:#25233f;font-weight:600;}
.rk-track{flex:1;height:12px;background:#f1f1f6;border-radius:8px;overflow:hidden;}
.rk-fill{height:100%;border-radius:8px;}
.rk-val{width:74px;text-align:right;font-size:12px;font-weight:700;}
.rec{background:#fff;border:1px solid #ececf3;border-left:5px solid #4f46e5;border-radius:14px;
  padding:26px 30px;margin-top:8px;box-shadow:0 8px 24px rgba(30,27,57,.06);
  font-size:15.5px;line-height:1.6;color:#25233f;}
.card{background:#fff;border:1px solid #ececf3;border-radius:14px;padding:20px 24px;
  box-shadow:0 6px 18px rgba(30,27,57,.05);}
.section-label{font-size:13px;font-weight:700;letter-spacing:.6px;color:#8b8aa0;
  text-transform:uppercase;margin:26px 0 10px;}
</style>
""", unsafe_allow_html=True)


def render_agents(ph, statuses):
    cards = ""
    for name, (role, emoji) in AGENT_META.items():
        state = statuses.get(name, "pending")
        cards += (f'<div class="agent {state}"><div class="emoji">{emoji}</div>'
                  f'<div class="name">{name}</div><div class="role">{role}</div>'
                  f'<div class="dot"></div></div>')
    ph.markdown(f'<div class="agents">{cards}</div>', unsafe_allow_html=True)


def render_risk_chart(scores: dict) -> str:
    rows = ""
    for cat, lvl in scores.items():
        val, color = LEVELS.get(str(lvl).upper(), (0, "#d7d7e2"))
        rows += (f'<div class="rk"><span class="rk-label">{cat}</span>'
                 f'<div class="rk-track"><div class="rk-fill" style="width:{int(val/3*100)}%;'
                 f'background:{color};"></div></div>'
                 f'<span class="rk-val" style="color:{color};">{str(lvl).upper()}</span></div>')
    return f'<div class="card">{rows}</div>'


def overall_risk(scores: dict) -> str:
    vals = [LEVELS.get(str(v).upper(), (0, ""))[0] for v in scores.values()]
    if not vals:
        return "N/A"
    m = max(vals)
    return {3: "Elevated", 2: "Moderate", 1: "Low"}.get(m, "N/A")


# ============================================================================
# UI
# ============================================================================
st.markdown("""
<div class="hero">
  <div class="badge">POWERED BY AZURE OPENAI · MULTI-AGENT</div>
  <h1>🧠 Synapse</h1>
  <p>Multi-Agent Business Intelligence & Decision Support — six specialist AI agents
  analyze your question, weigh the risks, and deliver one clear recommendation.</p>
</div>
""", unsafe_allow_html=True)

question = st.text_input("Your business question",
    placeholder="e.g. Sales dropped 20%. Should we cut price or run a promotion?")
go = st.button("Analyze", type="primary")

st.markdown('<div class="section-label">Agent Activity</div>', unsafe_allow_html=True)
agent_area = st.empty()
render_agents(agent_area, {})

if go and question:
    findings, statuses = {}, {}

    def run(name, prompt, user):
        statuses[name] = "running"; render_agents(agent_area, statuses)
        out = ask(prompt, user)
        statuses[name] = "done"; render_agents(agent_area, statuses)
        time.sleep(0.15)
        return out

    # Run the four specialists. (Teammates: to plug in a real agent, replace the
    # `run(...)` call for your agent with a call to your own function, e.g.
    #     findings["Analytics"] = analyze(question)  )
    for name, prompt in SPECIALISTS.items():
        findings[name] = run(name, prompt, question)
    findings["Risk"] = run("Risk", RISK_PROMPT,
                           f"Decision: {question}\n\nFindings:\n{_format(findings)}")
    strategy = run("Strategy", STRATEGY_PROMPT,
                   f"Question: {question}\n\nFindings:\n{_format(findings)}")

    st.session_state.update(findings=findings, strategy=strategy,
                            scores=risk_scores(findings))

if "strategy" in st.session_state:
    scores = st.session_state.get("scores", {})

    # metric tiles
    st.markdown('<div class="section-label">Summary</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="metrics">
      <div class="metric"><div class="v">6</div><div class="l">AGENTS CONSULTED</div></div>
      <div class="metric"><div class="v">{overall_risk(scores)}</div><div class="l">OVERALL RISK</div></div>
      <div class="metric"><div class="v">{DEPLOYMENT}</div><div class="l">MODEL</div></div>
    </div>
    """, unsafe_allow_html=True)

    if scores:
        st.markdown('<div class="section-label">Risk Profile</div>', unsafe_allow_html=True)
        st.markdown(render_risk_chart(scores), unsafe_allow_html=True)

    st.markdown('<div class="section-label">Recommendation</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="rec">{st.session_state["strategy"].replace(chr(10), "<br>")}</div>',
                unsafe_allow_html=True)

    with st.expander("See how each agent contributed"):
        for name, text in st.session_state["findings"].items():
            role, emoji = AGENT_META[name]
            st.markdown(f"**{emoji} {name} — {role}**")
            st.write(text)
