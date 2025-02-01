from flask import Blueprint, request, jsonify, current_app
import openai
import os
from app.models.user import UserProfile
from app.models.narrative import Narrative
from app.models.activity import Activity

ai_bp = Blueprint('ai', __name__)

CONTEXT_FILE = 'context.txt'

def load_context():
    if not os.path.exists(CONTEXT_FILE):
        return "No context available."
    with open(CONTEXT_FILE, 'r') as f:
        return f.read()

@ai_bp.route('/upload_context', methods=['POST'])
def upload_context():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    # Save the uploaded file as context.txt
    file.save(CONTEXT_FILE)
    return jsonify({"message": f"Context saved successfully in {CONTEXT_FILE}"}), 200

@ai_bp.route('/generate', methods=['POST'])
def generate():
    context = load_context()

    data = request.json
    section = data.get('section')
    if not section:
        return jsonify({"error": "Section is required"}), 400

    # Fetch elements based on the section
    section_elements = ""
    if section == "user_profile":
        section_elements = "\n".join(
            [f"- {profile.name} (Role: {profile.role})" for profile in UserProfile.query.all()]
        )
    elif section == "narrative":
        section_elements = "\n".join(
            [f"- {narrative.title} (Objective: {narrative.objective})" for narrative in Narrative.query.all()]
        )
    elif section == "activity":
        section_elements = "\n".join(
            [f"- {activity.description} (Assigned User: {activity.user_profile.name})" for activity in Activity.query.all()]
        )
    if not section_elements:
        section_elements = "No elements."

    # Generar el prompt para el modelo
    section_prompts = {
        "user_profile": """
        Based on the provided context, generate a new user profile including:
        - Name
        - Role
        - Behavior Pattern (a brief description of typical activities for this role).
        Return the profile in JSON format.
        """,
        "narrative": """
        Based on the provided context, generate a new narrative including:
        - Title
        - Objective
        - Attacker Profile (a description of the attacker's characteristics).
        - Duration (in days).
        Return the narrative in JSON format.
        """,
        "activity": """
        Based on the provided context, generate new activity including:
        - Description
        - Details (String describing the activity)
        Return the activity in JSON format with only the required fields(Description, details).
        """
    }

    if section not in section_prompts:
        return jsonify({"error": f"Invalid section '{section}'"}), 400

    messages = [
        {"role": "system", "content": "You are a helpful assistant that generates structured data based on context. Create new elements based on the provided context."},
        {"role": "user", "content": f"Context:\n{context}\n\nCurrent {section} Elements:\n{section_elements}\n\n{section_prompts[section]}"}
    ]
    print(messages)
    openai.api_key = current_app.config['OPENAI_API_KEY']

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        print(response.choices[0].message.content.strip())
        result = response.choices[0].message.content.strip()
        return jsonify({"response": result}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
