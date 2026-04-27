from crewai import Agent
from llm.factory import get_llm

security_agent = Agent(
    role="Cybersecurity Expert",
    goal="""
Identify and classify security vulnerabilities in code.
""",
    backstory="""
You are a cybersecurity engineer specializing in secure coding practices,
threat modeling, and vulnerability detection.
""",
    llm=get_llm("gemini"),
    verbose=False
)