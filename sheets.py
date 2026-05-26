import os
import json
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

def save_to_sheet(data):

    google_creds = os.getenv("GOOGLE_CREDS")

    creds_dict = json.loads(google_creds)

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        creds_dict,
        scope
    )

    client = gspread.authorize(creds)

    sheet = client.open("AI Leads CRM").sheet1

    sheet.append_row([
        datetime.now().isoformat(),
        data["lead_message"],
        data["follow_up"]["intent"],
        data["qualification"]["budget"],
        data["qualification"]["urgency"],
        data["score"]["lead_score"]
    ])