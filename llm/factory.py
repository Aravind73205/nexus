from crewai import LLM
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm(provider="gemini"):
    if provider == "gemini":
        return LLM(
            model="gemini/gemini-2.5-flash",
            api_key=os.getenv("GEMINI_API_KEY")
        )

    raise ValueError(f"Unsupported LLM provider: {provider}")