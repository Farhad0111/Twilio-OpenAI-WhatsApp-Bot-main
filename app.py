# app.py
import os
from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Groq client


app = FastAPI()
client=Groq(api_key=os.getenv("GROQ_API_KEY"))
@app.post("/whatsapp", response_class=PlainTextResponse)
async def whatsapp_reply(
    Body: str = Form(...),
    From: str = Form(...)
):
    """
    Twilio will POST form fields:
      - Body: the incoming message text
      - From: the sender's WhatsApp number
    """
    print(f"Incoming from {From}: {Body}")

    # Build TwiML response
    twilio_resp = MessagingResponse()
    msg = twilio_resp.message()

    try:
        # Send user message to Groq API
        chat_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # replace with the model you want
            messages=[{"role": "user", "content": Body}]
        )
        # Extract assistant reply
        reply_text = chat_response.choices[0].message.content.strip()
    except Exception as e:
        print("Groq API error:", e)
        reply_text = "Sorry, something went wrong. Please try again later."

    msg.body(reply_text)
    return str(twilio_resp)

# Optional root endpoint
def root():
    return {"status": "ok"}

@app.get("/")
async def health_check():
    return {"status": "ok"}
