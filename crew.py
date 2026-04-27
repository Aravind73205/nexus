from crewai import Crew

from agents.code_quality_agent import code_quality_agent
from agents.security_agent import security_agent
from agents.decision_agent import decision_agent

from tasks.analyze_code import analyze_code_quality
from tasks.review_security import review_security
from tasks.make_decision import make_review_decision

from hooks.read_file import read_file_hook

crew = Crew(
    agents=[code_quality_agent, security_agent, decision_agent],
    tasks=[analyze_code_quality, review_security, make_review_decision],
    memory=False,
    verbose=False
)

def run_review(file_path: str):
    inputs = {"file_path": file_path}
    inputs = read_file_hook(inputs)
    return crew.kickoff(inputs=inputs)