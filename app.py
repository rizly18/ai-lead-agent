from fastapi.middleware.cors import CORSMiddleware
from sheets import save_to_sheet
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from email_generator import generate_email
from email_sender import send_email
import json

load_dotenv()

app = FastAPI(title="AI Lead Automation API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# ---------- REQUEST SCHEMA ----------
class LeadRequest(BaseModel):
    name: str
    email: str
    message: str

class EmailRequest(BaseModel):
    to_email: str
    subject: str
    body: str

# ---------- API ENDPOINT ----------
@app.get("/")
def home():
    return {"message": "AI Lead Agent API is running."}

@app.post("/process-lead")
def process_lead(lead: LeadRequest):
    lead_name = lead.name
    lead_email = lead.email
    lead_message = lead.message

    # --- Follow-up Agent ---
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

    followup = json.loads(
        clean_json(llm.invoke(followup_prompt).content)
    )

    # --- Qualification Agent ---
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

    qualification = json.loads(
        clean_json(llm.invoke(qualification_prompt).content)
    )

    # --- Scoring Agent ---
    scoring_prompt = f"""
    You are a sales lead scoring AI.

    Based on this data:
    {qualification}

    Return ONLY JSON with keys:
    - lead_score (HOT / WARM / COLD)
    - confidence (0 to 1)
    - reason
    """

    scoring = json.loads(
        clean_json(llm.invoke(scoring_prompt).content)
    )

    # --- Email Generator Agent ---
    email = generate_email(lead_message)

    final_data = {
        "name": lead_name,
        "email": lead_email,
        "lead_message": lead_message,
        "follow_up": followup,
        "qualification": qualification,
        "score": scoring,
        "email_content": email
    }

    save_to_sheet(final_data)

    return final_data

@app.post("/send-email")
def send_email_endpoint(request: EmailRequest):

    send_email(
        request.to_email,
        request.subject,
        request.body
    )

    return {
        "status": "success",
        "message": "Email sent successfully"
    }
