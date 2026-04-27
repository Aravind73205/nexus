from crewai import Agent
from llm.factory import get_llm

code_quality_agent = Agent(
    role="Senior Code Quality Analyst",
    goal="""
Ensure code is clean, maintainable, and efficient.
""",
    backstory="""
You are a senior software engineer with deep expertise in clean code principles,
performance optimization, and maintainability.
""",
    llm=get_llm("gemini"),
    verbose=False
)