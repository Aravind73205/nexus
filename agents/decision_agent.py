from crewai import Agent
from llm.factory import get_llm

decision_agent = Agent(
    role="Technical Lead Reviewer",
    goal="""
Make final approval decisions based on analysis.
""",
    backstory="""
You are a senior technical lead responsible for approving production code.
""",
    llm=get_llm("gemini"),
    verbose=False
)