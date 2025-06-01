"""USSD utils."""

from collections import defaultdict

from src.models import User

ussd_sessions = {}
questions = {
    "start": {"message": "Weka umri wako (miaka):", "next": "age"},
    "age": {"message": "Weka jinsia yako (M/F):", "next": None},
}


def process_ussd(data: dict) -> str:
    phone_number = data.get("phoneNumber")
    session_id = data.get("sessionId")
    if not session_id:
        return "END Tafadhali jaribu tena baadae."
    if not phone_number:
        return "END Tafadhali toa nambari ya simu."

    if data.get("text") == "":
        return "CON Karibu AfyaChap\n1. Jisajili"
    elif data.get("text") == "1" or session_id in ussd_sessions:
        # check state of the session
        if session_id not in ussd_sessions:
            ussd_sessions[session_id] = {
                "phone_number": phone_number,
                "state": "start",
            }
            question = questions["start"]
            # update the session state to the next question
            ussd_sessions[session_id]["state"] = question["next"]
            return f"CON {question['message']}"
        # get current state of the session
        current_state = ussd_sessions[session_id]["state"]
        user_text = data.get("text", "").strip().split("*")[-1]
        if not current_state is None:
            print(ussd_sessions[session_id])
            responses = ussd_sessions[session_id].get("responses", {})
            User.create_user(
                phone_number=phone_number,
                age=int(responses.get("age", 0)),
                notice=responses.get("notice", ""),
            )
            return "END Hakuna swali zaidi. Endelea kutumia huduma zetu kwa AfyaChap."
        # update the session state based on the current state
        if "responses" not in ussd_sessions[session_id]:
            ussd_sessions[session_id]["responses"] = defaultdict(str)
        print(f"Current state: {current_state}, User text: {user_text}")
        ussd_sessions[session_id]["responses"].update({current_state: user_text})
        print(f"Updated responses: {ussd_sessions[session_id]['responses']}")
        response = questions.get(current_state, {"message": "END Hakuna swali zaidi."})
        return f"CON {response['message']}"
    return "END Tafadhali jaribu tena."
