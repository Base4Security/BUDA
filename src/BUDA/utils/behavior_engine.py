import requests
from flask import current_app

def generate_commands(narrative_id):
    """
    Calls the AI integration route to generate PowerShell commands dynamically.
    """
    ai_url = f"http://127.0.0.1:5000/ai/generate_commands/{narrative_id}"

    try:
        response = requests.post(ai_url)
        response.raise_for_status()

        ai_data = response.json()
        return ai_data.get("commands", ["Error: AI did not return commands"])

    except requests.exceptions.RequestException as e:
        return [f"Error: {str(e)}"]
