from dotenv import load_dotenv
from langchain_groq import ChatGroq
import json

load_dotenv()

# ---------- UTILS ----------
def clean_json(text: str) -> str:
    text = text.strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("No JSON found in AI output")
    return text[start:end + 1]

# ---------- LLM ----------
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2
)

# ---------- INPUT ----------
lead_message = "We are a startup looking for marketing services. Budget is around $1500 and we want to start ASAP."

print("\nLEAD MESSAGE:")
print(lead_message)

# ---------- AGENT 1: FOLLOW-UP ----------
followup_prompt = f"""
You are a professional sales assistant for a marketing agency.

Respond ONLY in valid JSON with keys:
- reply
- intent (interested / not_interested / unclear)

Rules:
- Polite
- Short
- Ask ONE follow-up question
- No emojis

Lead message:
{lead_message}
"""

followup_raw = llm.invoke(followup_prompt).content
followup = json.loads(clean_json(followup_raw))

print("\nFOLLOW-UP AGENT OUTPUT:")
print(followup)

# ---------- AGENT 2: QUALIFICATION ----------
qualification_prompt = f"""
You are a lead qualification AI.

Analyze the lead message and extract:

Return ONLY JSON with keys:
- budget (low / medium / high / unknown)
- urgency (low / medium / high / unknown)
- fit (good / average / bad)

Lead message:
{lead_message}
"""

qualification_raw = llm.invoke(qualification_prompt).content
qualification = json.loads(clean_json(qualification_raw))

print("\nQUALIFICATION AGENT OUTPUT:")
print(qualification)

# ---------- AGENT 3: SCORING ----------
scoring_prompt = f"""
You are a sales lead scoring AI.

Based on this data:
{qualification}

Return ONLY JSON with keys:
- lead_score (HOT / WARM / COLD)
- confidence (0 to 1)
- reason
"""

scoring_raw = llm.invoke(scoring_prompt).content
scoring = json.loads(clean_json(scoring_raw))

print("\nSCORING AGENT OUTPUT:")
print(scoring)

# ---------- FINAL RESULT ----------
final_result = {
    "lead_message": lead_message,
    "follow_up": followup,
    "qualification": qualification,
    "score": scoring
}

print("\nFINAL PIPELINE OUTPUT:")
print(json.dumps(final_result, indent=2))
