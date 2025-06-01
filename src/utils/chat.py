"""Chat Assistant Utilities."""

import os

import africastalking
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider
from pydantic_ai.settings import ModelSettings

load_dotenv()

text_model = "gemini-2.0-flash-lite"
voice_model = "models/gemini-2.0-flash-live-001"
model = GeminiModel(
    text_model, provider=GoogleGLAProvider(api_key=os.getenv("GEMINI_API_KEY"))
)

username = "sandbox"
api_key = os.getenv("AFRICASTALKING_API_KEY")
# Initialize the SDK
africastalking.initialize(username, api_key)

sms_client = africastalking.SMS


agent = Agent(
    model=model,
    settings=ModelSettings(
        max_tokens=1000,
        temperature=0.01,
    ),
    output_type=str,
    system_prompt=(
        "You are helpful assistant to help with healthcare related question that a users asks about First AID or mental health.",
        "You are to provide accurate and concise answers. If you don't know the answer, say 'I don't know'. You are to respond in the same language as used by user.",
        "Your services are limited to providing how to administer fisrt aid and a bit of information regarding mental health only. You are not a doctor and you cannot provide medical advice so let user know that information might be limited and might need to be verified with a medical professional.",
    ),
)


async def text_chat(data: dict) -> str:
    """Chat with the text model."""
    message = data["text"]
    response = await agent.run(message)

    sender_number = data["from"]
    short_code = data.get("to", "16038")
    # Send the response via SMS
    sms_client.send(response.output, [sender_number], sender_id=short_code)
    return response
