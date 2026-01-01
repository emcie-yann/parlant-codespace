# Agent that register customer hotel room bookings in Google Sheets
# Step 1: install the required packages `pip install gspread google-auth`
# Step 2: Login to Google Cloud Console and enaable Google Sheets API for your project
# Step 3: Create Service Account credentials, download the JSON file and upload to your Parlant project files
# Step 4: Create a Google Sheet with required columns (e.g., Check-in Date, Check-out Date, Room Type, Number of Guests)
# Step 5 : Share the Google Sheet with the service account email (found in the JSON file)


import asyncio
from datetime import datetime
from typing import Any
from google.oauth2.service_account import Credentials
import gspread
import parlant.sdk as p
from dotenv import load_dotenv
load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
JSON_PATH = 'service-account-path.json'  # Path to your service account JSON file
SHEET_ID = "GOOGLE_SHEET_ID" # Your Google Sheet ID

def write_to_google_sheet(sheet_id: str, row: list[str])->bool:
    creds = Credentials.from_service_account_file(
        JSON_PATH,
        scopes=SCOPES
    ) # type: ignore
    client = gspread.authorize(creds)
    worksheet = client.open_by_key(sheet_id).worksheet("BookTable") # <-- Change to your sheet name

    worksheet.append_row(row)
    return True

@p.tool
async def book_room(context: p.ToolContext, checkin:datetime, checkout:datetime, room_type:str, guests:int, full_name:str, email:str) -> p.ToolResult:
    
    row:list[Any] = [
        full_name,
        checkin.strftime("%Y-%m-%d"),
        checkout.strftime("%Y-%m-%d"),
        room_type,
        guests,
        email
    ]

    try:
        write_to_google_sheet(SHEET_ID, row)
    except Exception as e:
        return p.ToolResult(data={"Booked": False, "Error": f"Failed to write to Google Sheets: {e}"})
    
    return p.ToolResult(data={"Booked": True})
    

async def main() -> None:
    async with p.Server(
        session_store="local",
        port=8820,
        migrate=True,
        log_level=p.LogLevel.TRACE,
    ) as server:
        agent = await server.create_agent(
            name="Haven",
            description=(
                "You are a luxury hotel reservation specialist and digital concierge. "
                "You are sophisticated, polite, funny, and proactive. "
                "Your goal is to curate perfect stays, handle bookings efficiently, "
                "and manage guest logistics with a warm, welcoming demeanor."
            ),
        )
        
        journey = await agent.create_journey(
            title="Book Hotel Room",
            conditions=["The customer wants to book a room"],
            description="Guides the user through checking availability and confirming a hotel reservation.",
        )

        # Start -> Ask for Check-in and Check-out Dates
        s1 = await journey.initial_state.transition_to(
            chat_state="Ask the guest for their desired check-in and check-out dates."
        )

        s2 = await s1.target.transition_to(
            chat_state="Ask which room type they prefer (Standard, Deluxe, or Suite)."
        )
        
        s3 = await s2.target.transition_to(
            chat_state="Ask how many guests will be staying."
        )
        
        s4 = await s3.target.transition_to(
            chat_state="Ask for their full."
        )
        
        s5 = await s4.target.transition_to(
            chat_state="Ask for their email address."
        )

        # Book Room -> book_room(Tool)
        s6 = await s5.target.transition_to(
            tool_instruction="Book the room.",
            tool_state=book_room,
        )
        
        await s6.target.transition_to(
            condition="Room booking was successful.",
            chat_state="Notify the customer that their room has been successfully booked."
        )


asyncio.run(main())
