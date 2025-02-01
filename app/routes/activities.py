from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models.activity import Activity
from app.models.user import UserProfile
from app import db
import requests
import json

activities_bp = Blueprint('activities_bp', __name__)

@activities_bp.route('/', methods=['GET', 'POST'])
def manage_activities():
    if request.method == 'POST':
        # Recibir datos del formulario
        description = request.form.get('description')
        details = request.form.get('details')
        user_profile_id = int(request.form.get('user_profile_id'))

        # Crear y guardar la actividad
        new_activity = Activity(
            description=description,
            details=details,
            user_profile_id=user_profile_id
        )
        db.session.add(new_activity)
        db.session.commit()

        return redirect(url_for('activity_bp.manage_activities'))

    # Obtener todas las actividades y perfiles para mostrarlas
    activities = Activity.query.all()
    user_profiles = UserProfile.query.all()
    return render_template('activities.html', activities=activities, user_profiles=user_profiles)

@activities_bp.route('/edit/<int:activity_id>', methods=['GET', 'POST'])
def edit_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)

    if request.method == 'POST':
        # Actualizar datos de la actividad
        activity.description = request.form.get('description')
        activity.details = request.form.get('details')
        activity.user_profile_id = int(request.form.get('user_profile_id'))

        db.session.commit()
        return redirect(url_for('activity_bp.manage_activities'))

    # Renderizar el formulario de edición con los datos de la actividad
    user_profiles = UserProfile.query.all()
    return render_template('edit_activities.html', activity=activity, user_profiles=user_profiles)

@activities_bp.route('/delete/<int:activity_id>', methods=['POST'])
def delete_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    db.session.delete(activity)
    db.session.commit()
    return redirect(url_for('activity_bp.manage_activities'))

@activities_bp.route('/generate', methods=['POST'])
def generate_activity():
    data = request.json
    user_profile_id = data.get('user_profile_id')
    response = requests.post("http://localhost:5000/ai/generate", json={"section": "activity"})
    if response.status_code != 200:
        return jsonify({"error": "Failed to generate activity"}), 500
    try:
        profile_data = json.loads(response.json()["response"])
        
        # Recursive function to find keys regardless of case
        def search_keys(obj):
            description = None
            details = None
            
            if isinstance(obj, dict):
                for key, value in obj.items():
                    key_lower = key.lower()
                    if key_lower == "description":
                        description = value
                    elif key_lower == "details":
                        details = value
                    elif isinstance(value, (dict, list)):
                        # Recursively search nested objects or lists
                        sub_result = search_keys(value)
                        description = description or sub_result.get("description")
                        details = details or sub_result.get("details")
            elif isinstance(obj, list):
                for item in obj:
                    sub_result = search_keys(item)
                    description = description or sub_result.get("description")
                    details = details or sub_result.get("details")
            
            return {"description": description, "details": details}

        # Search for the keys in the parsed data
        result = search_keys(profile_data)

        description = result["description"]
        details = result["details"]

        new_profile = Activity(
            description=description,
            details=details,
            user_profile_id=user_profile_id
        )
        db.session.add(new_profile)
        db.session.commit()
        return jsonify({"message": "User Profile generated and saved successfully", "profile": profile_data}), 200
    except (KeyError, ValueError):
        return jsonify({"error": "Invalid response format from AI"}), 400