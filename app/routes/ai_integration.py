from flask import Blueprint, request, jsonify, current_app
import os
from app.models.user import UserProfile
from app.models.narrative import Narrative
from app.models.activity import Activity
import json

from app.utils.llm_utils import get_llm_response


ai_bp = Blueprint('ai', __name__)

CONTEXT_FILE = 'context.json'

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

@ai_bp.route('/generate/narrative', methods=['POST'])
def generate_narrative():
    data = request.json
    title = data.get('title')
    objective = data.get('objective')
    attacker_profile = data.get('attacker_profile')
    deception_activities = data.get('deception_activities')

    context = load_context()

    percentage_of_similarity = "100"

    # Generate the prompt
    narrative_prompt = """
                        Generate a new honey narrative
                        narrative_context { title: """ + f" {title}" + """, objective: """ + f" {objective}" + """, attacker_profile: """ + f" {attacker_profile}" + """, deception_activities: """ + f" {deception_activities}" + """ }
                        The narrative its a honey narrative that is a fake narrative that is used to attract attackers.
                        Use the context and thee narrative_context as a reference not to be copied. Do not use the context data.
                        The narrative is""" + f" {percentage_of_similarity}" + """% similar to the context.

                        The narrative must use the next base:
                        { title: "title", objective: "objective", attacker_profile: "attacker profile", deception_activities: "deception activities" }
                        - Title is the title of the narrative. Its a brief description of the narrative. Use the context as a reference for choosing a title.
                        - Objective is the objective of the narrative. Its a brief description of the narrative objective. Use the context as a reference for choosing an objective.
                        - Attacker Profile is a brief description of the attacker characteristics. Its a brief description of the attacker. Use the context as a reference for choosing an attacker profile.
                        - Deception Activities is a brief description of the activities in the narrative. Its a brief description of the activities in the narrative. Use the context as a reference for choosing deception activities.
                        
                        Return the narrative in JSON object in plain text.
                    """
    
    messages = [
        {"role": "system", "content": "You are a helpful cybersecurity proffesional that generates structured data"},
        {"role": "user", "content": f" Context:\n {context} \n\n {narrative_prompt}\n"}
    ]

    result = get_llm_response(messages)

    return jsonify({"message": result}), 200

@ai_bp.route('/generate/user_profile', methods=['POST'])
def generate_user_profile():
    data = request.json
    narrative_id = data.get('narrative_id')
    if not narrative_id:
        return jsonify({"error": "Missing narrative_id in request"}), 400
    narrative = Narrative.query.get_or_404(narrative_id)

    name = data.get('name')
    role = data.get('role')
    behavior_pattern = data.get('behavior_pattern')

    context = load_context()

    percentage_of_similarity = "100"

    # Generate the prompt
    user_profile_prompt = """
                            Generate a new honey user profile 
                            user_profile_context { complete_name: """ + f" {name}" + """, role: """ + f" {role}" + """, behavior_pattern: """ + f" {behavior_pattern}" + """ }
                            The user its a honey user that is a fake user that is used to attract attackers.
                            Use the context and thee user_profile_context as a reference not to be copied. Do not use the context data.
                            The user profile is""" + f" {percentage_of_similarity}" + """% similar to the context.
                            
                            The user profile must use the next base:
                            { complete_name: "name lastname", role: "organization role", behavior_pattern: "some pattern" }
                            - Name is the name and lastname of a user. Its a human name. Use the context as a reference for choosing a name.
                            - Role is the role of the user. Its a typical organization role. Use the context as a reference for choosing a role.
                            - The Behavior Pattern is a brief description of typical activities in the envinronment. It describe the user behavior in the system. Use the context as a reference for choosing a behavior pattern.

                            Return the profile in JSON object in plain text.
                        """

    messages = [
        {"role": "system", "content": "You are a helpful cybersecurity proffesional that generates structured data"},
        {"role": "user", "content": f" Context:\n {context} \n\n {user_profile_prompt}\n"}
    ]    

    result = get_llm_response(messages)

    return jsonify({"message": result}), 200

@ai_bp.route('/generate/activitytype', methods=['POST'])
def generate_activity():
    data = request.json
    user_profile_id = data.get('user_profile_id')
    if not user_profile_id:
        return jsonify({"error": "Missing user_profile_id in request"}), 400
    user_profile = UserProfile.query.get_or_404(user_profile_id)

    activity_type = data.get('activity_type')
    details = data.get('details')

    context = load_context()

    percentage_of_similarity = "100"

    # Generate the prompt
    activitytype_prompt = """
                        Generate a new honey activity type
                        activity_context { activity_type: """ + f" {activity_type}" + """, details: """ + f" {details}" + """ }
                        The activity type its a honey activity type that is a fake activity that is used to attract attackers.
                        Use the context and thee activity_context as a reference not to be copied. Do not use the context data.
                        The activity type is""" + f" {percentage_of_similarity}" + """% similar to the context.

                        The activity type must use the next base:
                        { activity_type: "activity_type", details: "details" }
                        - activity_type is the title of the type of a normal user activity based on the context elements. Its a brief description of the activity. Use the context as a reference for choosing a description.
                        - Details is a string describing the activity. Its a brief description of the activity. Use the context as a reference for choosing details.

                        Return the activity in JSON object in plain text.
                    """
    
    messages = [
        {"role": "system", "content": "You are a helpful cybersecurity proffesional that generates structured data"},
        {"role": "user", "content": f" Context:\n {context} \n\n {activitytype_prompt}\n"}
    ]

    result = get_llm_response(messages)

    return jsonify({"message": result}), 200

@ai_bp.route('/generate_commands/<int:narrative_id>', methods=['POST'])
def generate_ai_commands(narrative_id):
    """Generates PowerShell commands dynamically using AI based on a narrative."""
    
    narrative = Narrative.query.get(narrative_id)
    if not narrative:
        return jsonify({"error": "Narrative not found"}), 404

    # Organize User Profiles and Activity Types
    user_profiles_data = {}
    for profile in narrative.user_profiles:
        activity_types = [activity.activity_type for activity in profile.activities]
        user_profiles_data[profile.name] = activity_types

    percentage_of_similarity = narrative.percentage_of_similarity

    # Construct AI Prompt
    commands_prompt = f"""
        You are a cybersecurity expert generating PowerShell commands for a simulated cyber attack scenario.
        Based on the following details, suggest 3 relevant PowerShell commands for each user profile.

        - **Narrative Title:** {narrative.title}
        - **Objective:** {narrative.objective}
        - **Attacker Profile:** {narrative.attacker_profile}
        - **Percentage of Similarity:** {narrative.percentage_of_similarity}%

        The **percentage of similarity** defines how closely the commands should match the context:
        - **100% similarity** means commands must be highly aligned to the scenario, matching the exact attack techniques described.
        - **1% similarity** means commands should be loosely related, potentially exploratory or unexpected in this context.

        Provide structured output in the format:
        ```
        {{ "commands": [ {{ "user_profile": "User1", "activity_type": "Recon", "commands": ["cmd1", "cmd2", "cmd3"] }}, ... ] }}
        ```
    """

    # Add detailed breakdown per user profile
    for user, activities in user_profiles_data.items():
        commands_prompt += f"\n- **User Profile:** {user} \n  - Activity Types: {', '.join(activities)}\n"

    messages = [
        {"role": "system", "content": "You are a cybersecurity professional that generates structured JSON data."},
        {"role": "user", "content": f"{commands_prompt}\n"}
    ]

    result = get_llm_response(messages)
    
    # Extract and return structured JSON response
    try:
        ai_response = json.loads(result)
        return jsonify(ai_response)
    except (json.JSONDecodeError, KeyError):
        return jsonify({"error": "AI Response Failed or returned unstructured data"}), 500
