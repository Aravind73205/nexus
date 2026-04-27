from crewai import Task
from agents.decision_agent import decision_agent
from guardrails.decision_guardrail import review_decision_guardrail


make_review_decision = Task(
    description="""
You are given code and its analysis.

Based on:
- Code quality issues
- Security vulnerabilities

Make a FINAL decision:

APPROVE if:
- No high-risk issues
- Code is reasonably clean

REJECT if:
- Any high-risk vulnerability exists
- Critical issues found

Explain clearly:
- Why you approved or rejected
- Key issues influencing decision

Output MUST clearly include:
- "APPROVE" or "REJECT"
- Justification
""",
    expected_output="Final approval or rejection decision",
    agent=decision_agent,  
    markdown=True,
    guardrails=[review_decision_guardrail]
)