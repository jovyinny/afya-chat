"""API for the application."""

from fastapi import BackgroundTasks, FastAPI, Request, Response

from src.models import User
from src.utils.chat import sms_client, text_chat
from src.utils.tasks import extract_form_data
from src.utils.ussd import process_ussd

app = FastAPI()


@app.post("/voice/callback")
async def handle_voice(request: Request):
    try:
        # Process the voice data here
        data = await request.body()
        data = extract_form_data(data)

        print("Received voice data:", data)
        # always is xml data
        return Response(
            content="""<?xml version="1.0" encoding="UTF-8"?>
            <Response>
                <Say voice= "en-US-Wavenet-C">
                <speak>My speech content.</speak>
                </Say>
            </Response>
            """,
            media_type="application/xml",
            headers={"Content-Type": "text/plain"},
        )
    except Exception as e:
        print("Error processing voice data:", str(e))
        return Response(
            content="""<?xml version="1.0"?>
           <Response>
                <Say voice= "en-US-Wavenet-C">
                <speak>My speech content.</speak>
                </Say>
            </Response>
            """,
            media_type="application/xml",
            headers={"Content-Type": "text/plain"},
        )


@app.post("/sms/callback")
async def handle_sms(request: Request, background_tasks: BackgroundTasks):
    try:
        # Process the SMS data here
        data = await request.body()
        data = extract_form_data(data)

        print("Received SMS data:", data)
        phone_number = data.get("from")
        short_code = data.get("to", "16038") 
        is_registered = User.check_user_exists(phone_number)
        if not is_registered:
            background_tasks.add_task(
                sms_client.send,
                "Tafadhali jisali kupitia *384*21038# ili kuweza kuendelea na huduma za AfyaChap.",
                [phone_number],
                sender_id=short_code,
            )
            return {"status": "error", "message": "User not registered."}
        # For demonstration, we just return the received data
        background_tasks.add_task(text_chat, data)
        return {"status": "success", "data": data}
    except Exception as e:
        print("Error processing SMS data:", str(e))
        return {"status": "error", "message": str(e)}


@app.post("/ussd/callback")
async def handle_ussd(request: Request):
    try:
        # Process the USSD data here
        data = await request.body()
        data = extract_form_data(data)
        print("Received USSD data:", data)
        phone_number = data.get("phoneNumber")
        if not phone_number:
            return Response(
                content="END Hakuna nambari ya simu iliyotolewa.",
                media_type="text/plain",
                headers={"Content-Type": "text/plain"},
            )
        response = process_ussd(data)

        return Response(
            content=response,
            media_type="text/plain",
            headers={"Content-Type": "text/plain"},
        )

    except Exception as e:
        print("Error processing USSD data:", str(e))
        return Response(
            content="END Tafadhali jaribu tena. Developer is cooked",
            media_type="text/plain",
            headers={"Content-Type": "text/plain"},
        )
