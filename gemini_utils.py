import os
from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not api_key or api_key in ["YOUR_GEMINI_API_KEY", "my_key"]:
    raise ValueError("GEMINI_API_KEY is missing or invalid in .env file!")

client = genai.Client(api_key=api_key)
MODEL_NAME = "gemini-1.5-flash"


class BudgetBreakdownItem(BaseModel):
    category: str
    estimated_cost: float
    description: str


class BudgetResponse(BaseModel):
    total_budget: float
    allocated_budget: float
    remaining_budget: float
    breakdown: List[BudgetBreakdownItem]
    suggestions: List[str]


GENAI_CONFIG = types.GenerateContentConfig(
    response_mime_type="application/json",
    response_schema=BudgetResponse,
)


async def generate_budget_plan(prompt: str):
    """Gemini-கிட்ட prompt அனுப்பி, structured budget response வாங்குதல்."""
    response = await client.aio.models.generate_content(
        model=MODEL_NAME, contents=prompt, config=GENAI_CONFIG
    )
    return response.parsed if hasattr(response, "parsed") and response.parsed else response.text