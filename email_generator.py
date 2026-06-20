from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3
)

def generate_email(lead_message):

    prompt = f"""
    You are an expert sales representative.

    A lead sent this message:

    {lead_message}

    Write a professional follow-up email.

    Requirements:
    - Friendly
    - Professional
    - Short
    - Encourage a meeting

    Return ONLY the email.
    """

    response = llm.invoke(prompt)

    return response.content