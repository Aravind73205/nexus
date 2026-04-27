from crewai import Task
from pydantic import BaseModel
from agents.code_quality_agent import code_quality_agent


class CodeQualityJSON(BaseModel):
    issues: list[str]
    suggestions: list[str]


analyze_code_quality = Task(
    description="""
You are given source code in {file_content}.

Perform a deep code quality analysis.

Focus on:
- Code smells (duplicate code, long functions, poor naming)
- Bad practices (hardcoding, lack of modularity)
- Inefficiencies (unoptimized loops, unnecessary computations)
- Readability and maintainability issues

For each issue:
- Clearly describe the problem
- Suggest an improvement

Return structured JSON:
{
  "issues": [...],
  "suggestions": [...]
}
""",
    expected_output="Structured code quality analysis",
    agent=code_quality_agent,
    output_json=CodeQualityJSON
)