from crewai import Task
from pydantic import BaseModel
from agents.security_agent import security_agent
from guardrails.security_guardrail import security_review_output_guardrail


class SecurityVulnerability(BaseModel):
    description: str
    risk_level: str
    evidence: str


class ReviewSecurityJSON(BaseModel):
    security_vulnerabilities: list[SecurityVulnerability]
    blocking: bool
    highest_risk: str
    security_recommendations: list[str]


review_security = Task(
    description="""
You are given source code in {file_content}.

Perform a deep security analysis.

Focus on:
- Hardcoded secrets (passwords, API keys)
- Injection vulnerabilities (SQL, command injection)
- Unsafe file handling
- Insecure API usage
- Authentication and authorization issues

For each vulnerability:
- Provide description
- Assign risk level (low, medium, high)
- Provide concrete evidence from code

Also:
- Identify the highest risk level
- Suggest remediation steps

Return structured JSON:
{
  "security_vulnerabilities": [...],
  "blocking": true/false,
  "highest_risk": "low|medium|high",
  "security_recommendations": [...]
}
""",
    expected_output="Structured security analysis",
    agent=security_agent,
    output_json=ReviewSecurityJSON,
    guardrails=[security_review_output_guardrail]
)